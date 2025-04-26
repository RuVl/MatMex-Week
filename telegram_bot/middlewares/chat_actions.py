from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.dispatcher.middlewares.user_context import EVENT_CHAT_KEY, EVENT_FROM_USER_KEY
from aiogram.types import Message, TelegramObject
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

from middlewares import LOGGING_KEY
from .utils import MessageActionWrapper


class ChatActionsMw(BaseMiddleware):
	"""
	Middleware to automatically show typing/upload actions during handler execution.
	Uses handler flags to determine what actions to show.
	"""

	def __init__(
			self,
			flag_name: str = 'chat_action',
			*,
			default_typing_speed: float = 150.0,
			default_max_delay: float = 0.75,
			default_max_upload_delay: float = 1.0,
			default_adaptive: bool = True,
			enabled: bool = True,
			active_by_default: bool = True,
	):
		self.flag_name = flag_name
		self._enabled = enabled
		self._active_by_default = active_by_default

		self.default_config = {
			"max_delay": float(default_max_delay),
			"typing_speed": float(default_typing_speed),
			"adaptive": bool(default_adaptive),
			"max_upload_delay": float(default_max_upload_delay),
		}

		self.logger = get_logger()

	async def __call__(
			self,
			handler: Callable,
			event: TelegramObject,
			data: dict[str, Any],
	) -> Any:
		# Skip if middleware is disabled
		if not self._enabled:
			return await handler(event, data)

		logger: FilteringBoundLogger = data.get(LOGGING_KEY, self.logger)

		# Check if the event type is supported
		if not isinstance(event, Message):
			await logger.awarning(
				"Unexpected event type",
				middleware=self.__class__.__name__,
				event_type=type(event).__name__
			)
			return await handler(event, data)

		# Check if the flag is set for this handler
		flag = get_flag(data, self.flag_name, default=self._active_by_default)
		if not flag:
			return await handler(event, data)

		# Parse the flag configuration
		cfg = await self._parse_flag(flag, logger)
		if cfg is None:
			return await handler(event, data)

		# Set logger from DI
		cfg.setdefault('log', data.get(LOGGING_KEY))

		# Create wrapped event
		wrapped_event = event
		wrapped_event = MessageActionWrapper(wrapped_event, **cfg)

		# Update dependencies in data
		data["event"] = wrapped_event
		data[EVENT_FROM_USER_KEY] = wrapped_event.from_user
		data[EVENT_CHAT_KEY] = wrapped_event.chat

		return await handler(wrapped_event, data)

	async def _parse_flag(self, flag_value: Any, logger: FilteringBoundLogger) -> dict[str, Any] | None:
		"""
		Parse the flag value into configuration dictionary.
		Returns None if the flag value is invalid.
		"""

		# Validate flag value type
		if not isinstance(flag_value, (dict, bool)):
			await logger.awarning("Invalid chat action flag", flag_name=self.flag_name, flag_value=str(flag_value))
			return None

		# Convert True to empty dict for default values
		if flag_value is True:
			return self.default_config.copy()

		if flag_value is False:
			return None

		# Return configuration with defaults for missing values		
		for key, value in self.default_config.items():
			if isinstance(flag_value, dict):
				flag_value.setdefault(key, value)

		return flag_value
