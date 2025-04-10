from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.types import TelegramObject, User
from structlog import get_logger
from structlog.typing import FilteringBoundLogger


class LoggingMiddleware(BaseMiddleware):
	def __init__(self, middleware_key: str = 'log'):
		self.logger: FilteringBoundLogger = get_logger()
		self.middleware_key = middleware_key

	@staticmethod
	def get_user_context(user: User) -> dict:
		"""Creates a context dictionary with user information for logging."""

		context = {}
		if user:
			context.update({
				"user_id": user.id,
				"username": user.username,
				"full_name": f"{user.first_name} {user.last_name or ''}".strip(),
			})
		return context

	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: Dict[str, Any],
	) -> Any:
		telegram_user = data.get(EVENT_FROM_USER_KEY)
		user_context = self.get_user_context(telegram_user) if telegram_user else {}

		log = self.logger.bind(**user_context)
		data[self.middleware_key] = log

		handler_name = handler.__name__ if hasattr(handler, "__name__") else str(handler)
		await log.adebug("handler-called", handler=handler_name)

		try:
			result = await handler(event, data)
			await log.adebug("handler-completed")
			return result
		except Exception as e:
			await log.aerror("handler-error", error=str(e), handler=handler_name)
			raise
