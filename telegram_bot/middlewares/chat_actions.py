from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.dispatcher.middlewares.user_context import EVENT_CHAT_KEY, EVENT_FROM_USER_KEY
from aiogram.types import CallbackQuery, Message, TelegramObject
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

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

		# Check if the event type is supported
		if not isinstance(event, (Message, CallbackQuery)):
			logger: FilteringBoundLogger = data.get('log', self.logger)
			await logger.awarning(
				"Unexpected event type",
				middleware=self.__class__.__name__,
				event_type=type(event).__name__
			)
			return await handler(event, data)

		# Check if the flag is set for this handler
		flag = get_flag(data, self.flag_name)
		if flag is None:
			return await handler(event, data)

		# Parse the flag configuration
		cfg = self._parse_flag(flag)
		if cfg is None:
			logger: FilteringBoundLogger = data.get('log', self.logger)
			await logger.awarning(
				"Invalid chat action flag",
				flag_name=self.flag_name,
				flag_value=str(flag)
			)
			return await handler(event, data)

		# Set logger from DI
		cfg.setdefault('log', data.get('log'))

		# Wrap message or callback query message with action wrapper
		try:
			# Create wrapped event
			wrapped_event = event
			if isinstance(wrapped_event, CallbackQuery):
				wrapped_event.message = MessageActionWrapper(wrapped_event.message, **cfg)
			else:
				wrapped_event = MessageActionWrapper(wrapped_event, **cfg)

			# Update dependencies in data
			data["event"] = wrapped_event
			data[EVENT_FROM_USER_KEY] = wrapped_event.from_user
			data[EVENT_CHAT_KEY] = wrapped_event.chat

			return await handler(wrapped_event, data)

		except Exception as e:
			await self.logger.aerror(
				"Error in chat action middleware",
				error=str(e),
				middleware=self.__class__.__name__
			)
			# Fall back to normal handler execution without wrapper
			return await handler(event, data)

	def _parse_flag(self, flag_value: Any) -> dict[str, Any] | None:
		"""
		Parse the flag value into configuration dictionary.
		Returns None if the flag value is invalid.
		"""
		# Convert True to empty dict for default values
		if flag_value is True:
			flag_value = {}

		# Validate flag value type
		if not isinstance(flag_value, dict):
			return None

		# Return configuration with defaults for missing values
		return {
			"max_delay": float(flag_value.get("max_delay", self._default_max_delay)),
			"typing_speed": float(flag_value.get("typing_speed", self._default_typing_speed)),
			"adaptive": bool(flag_value.get("adaptive", self._default_adaptive)),
			"max_upload_delay": float(flag_value.get("max_upload_delay", self._default_max_upload_delay)),
		}
