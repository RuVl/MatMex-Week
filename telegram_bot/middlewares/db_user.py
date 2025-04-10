import pickle
from datetime import timedelta
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY, EVENT_CHAT_KEY
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import TelegramObject, User, Chat
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

from database import async_session, models
from database.methods import get_user_by_telegram_id
from includes import get_storage


class DBUserMiddleware(BaseMiddleware):
	"""Get user from db or cache if event from user"""

	def __init__(self, /,
	             prefix: str = 'db_user',
	             key: str = 'telegram_id',
	             middleware_key: str = 'cached_user',
	             cache_expire: timedelta = timedelta(minutes=5),
	             ):
		self.storage = get_storage(key_builder_prefix=prefix, data_ttl=cache_expire)

		self.key = key
		self.middleware_key = middleware_key

		self.logger: FilteringBoundLogger = get_logger()

	async def get_db_user(self, storage_key: StorageKey) -> models.User:
		user = None
		try:
			storage_data = await self.storage.get_data(storage_key)
			cached_user = storage_data.get(self.key)
			if cached_user:
				return pickle.loads(cached_user)

			async with async_session() as session:
				user = await get_user_by_telegram_id(session, storage_key.user_id)
				if user:
					storage_data.update({self.key: pickle.dumps(user)})
					await self.storage.set_data(storage_key, storage_data)

		except Exception as e:
			await self.logger.awarning(f"{self.__class__.__name__} error: {e}")

		return user

	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: Dict[str, Any],
	) -> Any:
		# check if event from user
		tg_user: User = data[EVENT_FROM_USER_KEY]
		chat: Chat = data[EVENT_CHAT_KEY]

		if tg_user is None or chat is None:
			await self.logger.awarning(f'No EVENT_FROM_USER_KEY or EVENT_CHAT_KEY provided by event for check user privileges! Skip checking.')
			return await handler(event, data)

		storage_key = StorageKey(bot_id=event.bot, chat_id=chat.id, user_id=tg_user.id)
		data[self.middleware_key] = await self.get_db_user(storage_key)

		return await handler(event, data)

	async def close(self) -> None:
		await self.storage.close()
