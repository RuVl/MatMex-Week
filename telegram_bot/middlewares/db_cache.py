import base64
import pickle
from datetime import timedelta
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY, EVENT_CHAT_KEY
from aiogram.types import TelegramObject, User, Chat
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

from database import async_session, models
from database.methods import get_user_by_telegram_id
from includes import get_redis


def dumps_model(user: models.Base) -> str:
	"""Serialize the ORM user object into base64 string"""
	return base64.b64encode(pickle.dumps(user)).decode("utf-8")


def loads_model(data: str) -> models.Base:
	"""Deserialize the ORM user object from base64 string"""
	return pickle.loads(base64.b64decode(data))


class UserCacheMw(BaseMiddleware):
	"""Middleware to load and cache user info from the DB in Redis."""

	def __init__(self, /,
	             redis_prefix: str = 'cached_user',
	             ttl: timedelta = timedelta(minutes=5),
	             middleware_key: str = 'cached_user',
	             ):
		self.redis = get_redis(decode_responses=True)
		self.prefix = redis_prefix
		self.ttl_seconds = int(ttl.total_seconds())
		self.middleware_key = middleware_key

		self.logger: FilteringBoundLogger = get_logger()

	def _make_redis_key(self, telegram_id: int) -> str:
		return f"{self.prefix}:{telegram_id}"

	async def get_db_user(self, telegram_id: int) -> models.User:
		redis_key = self._make_redis_key(telegram_id)

		try:
			cached_data = await self.redis.get(redis_key)
			if cached_data is not None:
				return loads_model(cached_data)

			await self.logger.adebug("User not found in cache - load from database", telegram_id=telegram_id)
			async with async_session() as session:
				user = await get_user_by_telegram_id(session, telegram_id)
				if user:
					await self.redis.set(redis_key, dumps_model(user), ex=self.ttl_seconds)
				return user

		except Exception as e:
			await self.logger.awarning(f"{self.__class__.__name__} error: {e}")
			return None

	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: Dict[str, Any],
	) -> Any:
		tg_user: User = data.get(EVENT_FROM_USER_KEY)
		chat: Chat = data.get(EVENT_CHAT_KEY)

		if tg_user is None or chat is None:
			await self.logger.awarning(f"{self.__class__.__name__}: EVENT_FROM_USER_KEY or EVENT_CHAT_KEY not found, skipping.")
			return await handler(event, data)

		user = await self.get_db_user(tg_user.id)
		data[self.middleware_key] = user

		return await handler(event, data)

	async def close(self) -> None:
		await self.redis.close()
