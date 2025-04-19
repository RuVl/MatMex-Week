import time
import types
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from structlog import get_logger
from structlog.typing import FilteringBoundLogger


class LoggingMw(BaseMiddleware):
	def __init__(self, middleware_key: str = 'log', *, patch_fsm: bool = True):
		self.logger: FilteringBoundLogger = get_logger()
		self.middleware_key = middleware_key
		self.patch_fsm = patch_fsm

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

	def patch_fsm_methods(self, fsm: FSMContext, log: FilteringBoundLogger):
		"""Monkey patch fsm methods."""

		if not self.patch_fsm:
			return

		original_set_state = fsm.set_state

		async def set_state_with_logging(_, state):
			await log.adebug("state-changed", state="cleared" if state is None else str(state.state))
			return await original_set_state(state)

		fsm.set_state = types.MethodType(set_state_with_logging, fsm)

	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: Dict[str, Any],
	) -> Any:
		telegram_user = data.get(EVENT_FROM_USER_KEY)
		user_context = self.get_user_context(
			telegram_user) if telegram_user else {}

		log = self.logger.bind(**user_context)
		data[self.middleware_key] = log

		# Пытаемся получить настоящее имя хэндлера
		handler_obj = data.get("handler")
		handler_name = (
			getattr(handler_obj.callback, "__name__",
			        str(handler_obj.callback))
			if handler_obj and hasattr(handler_obj, "callback") else
			getattr(handler, "__name__", str(handler))
		)
		await log.adebug("handler-called", handler=handler_name)

		# Patch FSMContext methods if available
		state: FSMContext = data.get("state")
		if state:
			self.patch_fsm_methods(state, log)

		try:
			start = time.perf_counter()
			result = await handler(event, data)
			end = time.perf_counter()

			await log.adebug("handler-completed", handler=handler_name, seconds=format(end - start, '.3'))
			return result
		except Exception as e:
			await log.aerror("handler-error", error=str(e), handler=handler_name)
			raise
