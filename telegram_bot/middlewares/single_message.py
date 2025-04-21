import asyncio
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import skip
from aiogram.types import CallbackQuery, Message, TelegramObject


class SingleMessageMw(BaseMiddleware):
	def __init__(self, timeout: float = 0.1):
		self.active_users: dict[int, asyncio.Lock] = {}
		self.timeout = timeout  # максимальное время ожидания между сообщениями

	async def __call__(
			self,
			handler: Callable[[TelegramObject, dict[str, Any]], Any],
			event: TelegramObject,
			data: dict[str, Any],
	) -> Any:
		if isinstance(event, (Message, CallbackQuery)):
			user_id = event.from_user.id

			# Получаем или создаем Lock для пользователя
			user_lock = self.active_users.setdefault(user_id, asyncio.Lock())

			if user_lock.locked():
				return skip()

			async with user_lock:
				try:
					return await handler(event, data)
				finally:
					await asyncio.sleep(self.timeout)  # пауза перед разрешением следующего сообщения
