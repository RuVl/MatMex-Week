import base64
import pickle
from datetime import timedelta
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import extract_flags
from aiogram.dispatcher.middlewares.user_context import EVENT_CHAT_KEY, EVENT_FROM_USER_KEY
from aiogram.types import Chat, TelegramObject, User
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
	             no_cache_flag: str = 'no_cache',
	             disable_cache_flag: str = 'disable_cache',
	             ):
		self.redis = get_redis(decode_responses=True)
		self.prefix = redis_prefix
		self.ttl_seconds = int(ttl.total_seconds())
		self.middleware_key = middleware_key
		self.no_cache_flag = no_cache_flag
		self.disable_cache_flag = disable_cache_flag

		self.logger: FilteringBoundLogger = get_logger()

	def _make_redis_key(self, telegram_id: int) -> str:
		return f"{self.prefix}:{telegram_id}"

	async def get_db_user(self, telegram_id: int, use_cache: bool = True) -> models.User | None:
		"""Get user from cache or database and update cache if needed"""
		try:
			if use_cache:
				redis_key = self._make_redis_key(telegram_id)

				# Try to get from cache first
				cached_data = await self.redis.get(redis_key)
				if cached_data is not None:
					return loads_model(cached_data)

				# Not in cache, get from the database
				await self.logger.adebug("User not found in cache - loading from database", telegram_id=telegram_id)

			async with async_session() as session:
				user = await get_user_by_telegram_id(session, telegram_id)
				if user:
					# Cache the user data
					await self.redis.set(redis_key, dumps_model(user), ex=self.ttl_seconds)
				return user

		except Exception as e:
			await self.logger.aerror(
				"Error retrieving user",
				telegram_id=telegram_id,
				error=str(e),
				middleware=self.__class__.__name__
			)
			return None

	async def __call__(
			self,
			handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: dict[str, Any],
	) -> Any:
		# Check if the flag is set for this handler
		flags = extract_flags(handler)
		if flags.get(self.disable_cache_flag, False):
			return await handler(event, data)

		tg_user: User = data.get(EVENT_FROM_USER_KEY)
		chat: Chat = data.get(EVENT_CHAT_KEY)

		if tg_user is None or chat is None:
			await self.logger.awarning(
				"Missing user or chat data",
				middleware=self.__class__.__name__,
				has_user=tg_user is not None,
				has_chat=chat is not None
			)
			return await handler(event, data)

		use_cache = not flags.get(self.no_cache_flag, False)
		user = await self.get_db_user(tg_user.id, use_cache)
		data[self.middleware_key] = user

		return await handler(event, data)

	async def close(self) -> None:
		await self.redis.close()
