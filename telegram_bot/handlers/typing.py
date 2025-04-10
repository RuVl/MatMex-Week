import asyncio
from contextlib import asynccontextmanager
from typing import Any

from aiogram.enums import ChatAction
from aiogram.types import Message

from env import TelegramKeys


class TypingMessage:
	def __init__(self, msg: Message,
	             max_delay: float = 3.0,
	             typing_speed: float = 20.0,
	             adaptive: bool = True,
	             enabled: bool = True):
		self._msg = msg
		self._max_delay = max_delay
		self._speed = typing_speed
		self._adaptive = adaptive
		self._enabled = enabled

	def __getattr__(self, name: str) -> Any:
		orig_attr = getattr(self._msg, name)

		# Если это метод и начинается с "answer", "edit" или "reply", оборачиваем
		if self._enabled and callable(orig_attr) and (
				name.startswith('answer') or
				name.startswith('edit') or
				name.startswith('reply')
		):
			async def wrapped(*args, **kwargs):
				await self._msg.bot.send_chat_action(self._msg.chat.id, ChatAction.TYPING)
				delay = self._calculate_delay(*args, **kwargs)
				await asyncio.sleep(delay)
				return await orig_attr(*args, **kwargs)

			return wrapped

		return orig_attr  # Иначе — просто прокидываем

	def _calculate_delay(self, *args, **kwargs) -> float:
		if not self._adaptive:
			return self._max_delay

		text = self._extract_text(*args, **kwargs)
		if not text:
			return self._max_delay  # задержка, если текста нет

		calculated = len(text) / self._speed
		return min(calculated, self._max_delay)

	@staticmethod
	def _extract_text(*args, **kwargs) -> str | None:
		# Ищем в позиционных и именованных аргументах
		for key in ('text', 'caption'):
			if key in kwargs:
				return kwargs[key]

		# Пробуем достать из позиционных, если текст — первый аргумент
		if args and isinstance(args[0], str):
			return args[0]

		return None


@asynccontextmanager
async def send_typing(msg: Message, max_delay=5.0, speed=35.0, adaptive=True):
	yield TypingMessage(
		msg,
		max_delay=max_delay,
		typing_speed=speed,
		adaptive=adaptive,
		enabled=not TelegramKeys.WITHOUT_TYPING
	)
