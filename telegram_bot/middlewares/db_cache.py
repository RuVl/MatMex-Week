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
from middlewares import LOGGING_KEY


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
	             drop_cache_flag: str = 'drop_cache',
	             disable_cache_flag: str = 'disable_cache',
	             ):
		self.redis = get_redis(decode_responses=True)
		self.prefix = redis_prefix
		self.ttl_seconds = int(ttl.total_seconds())
		self.middleware_key = middleware_key
		self.drop_cache_flag = drop_cache_flag
		self.disable_cache_flag = disable_cache_flag

		self.logger: FilteringBoundLogger = get_logger()

	def _make_redis_key(self, telegram_id: int) -> str:
		return f"{self.prefix}:{telegram_id}"

	async def get_db_user(self, telegram_id: int, drop_cache: bool = True, logger: FilteringBoundLogger = None) -> models.User | None:
		"""Get user from cache or database and update cache if needed"""
		redis_key = self._make_redis_key(telegram_id)

		try:
			if not drop_cache:
				# Try to get from cache first
				cached_data = await self.redis.get(redis_key)
				if cached_data is not None:
					return loads_model(cached_data)

				# Not in cache, get from the database
				if logger is not None:
					await logger.adebug("User not found in cache", telegram_id=telegram_id)
			else:
				if logger is not None:
					await logger.adebug("Cache dropped", telegram_id=telegram_id)

			async with async_session() as session:
				user = await get_user_by_telegram_id(session, telegram_id)
				if user:
					# Cache the user data
					await self.redis.set(redis_key, dumps_model(user), ex=self.ttl_seconds)
				return user

		except Exception as e:
			if logger is not None:
				await logger.aerror("Error retrieving user", telegram_id=telegram_id, error=str(e))
			return None

	async def __call__(
			self,
			handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: dict[str, Any],
	) -> Any:
		# Check if the flag is set for this handler
		flags = extract_flags(data)
		if flags.get(self.disable_cache_flag, False):
			return await handler(event, data)

		tg_user: User = data.get(EVENT_FROM_USER_KEY)
		chat: Chat = data.get(EVENT_CHAT_KEY)

		logger: FilteringBoundLogger = data.get(LOGGING_KEY, self.logger)

		if tg_user is None or chat is None:
			await logger.awarning("Missing user or chat data", has_user=tg_user is not None, has_chat=chat is not None)
			return await handler(event, data)

		drop_cache = flags.get(self.drop_cache_flag, False)
		user = await self.get_db_user(tg_user.id, drop_cache, logger)
		data[self.middleware_key] = user

		return await handler(event, data)

	async def close(self) -> None:
		await self.redis.close()
