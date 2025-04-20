from typing import Callable, Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY, EVENT_CHAT_KEY
from aiogram.types import Message, CallbackQuery, TelegramObject
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

from .utils import MessageActionWrapper


class ChatActionsMw(BaseMiddleware):
	def __init__(
			self,
			flag_name: str = 'chat_action',
			*,
			default_typing_speed: float = 70.0,
			default_max_delay: float = 0.75,
			default_max_upload_delay: float = 1.0,
			default_adaptive: bool = True,
			enabled: bool = True
	):
		self.flag_name = flag_name
		self._enabled = enabled

		self._default_typing_speed = default_typing_speed
		self._default_max_delay = default_max_delay
		self._default_max_upload_delay = default_max_upload_delay
		self._default_adaptive = default_adaptive

	async def __call__(
			self,
			handler: Callable,
			event: TelegramObject,
			data: dict[str, Any],
	) -> Any:
		if not isinstance(event, (Message, CallbackQuery)):
			raise RuntimeError(
				f"{ChatActionsMw.__name__} got an unexpected event type!")

		if not self._enabled:
			return await handler(event, data)

		flag = get_flag(data, self.flag_name)
		if flag is None:
			return await handler(event, data)

		cfg = self._parse_flag(flag)
		if cfg is None:
			logger: FilteringBoundLogger = data.get('log', get_logger())
			await logger.awarning(f"Wrong flag value for {self.__class__.__name__}", flag_name=self.flag_name)
			return await handler(event, data)

		# Set logger from DI
		cfg.setdefault('log', data.get('log'))

		# Wrap message
		wrapped = event
		if isinstance(wrapped, CallbackQuery):
			wrapped.message = MessageActionWrapper(wrapped.message, **cfg)
		else:
			wrapped = MessageActionWrapper(wrapped, **cfg)

		# for DI
		data["event"] = wrapped
		data[EVENT_FROM_USER_KEY] = wrapped.from_user
		data[EVENT_CHAT_KEY] = wrapped.chat

		return await handler(wrapped, data)

	def _parse_flag(self, flag_value: Any) -> dict[str, Any] | None:
		if flag_value is True:
			flag_value = {}

		if not isinstance(flag_value, dict):
			return None

		return {
			"max_delay": float(flag_value.get("max_delay", self._default_max_delay)),
			"typing_speed": float(flag_value.get("typing_speed", self._default_typing_speed)),
			"adaptive": bool(flag_value.get("adaptive", self._default_adaptive)),
			"max_upload_delay": float(flag_value.get("max_upload_delay", self._default_max_upload_delay)),
		}
