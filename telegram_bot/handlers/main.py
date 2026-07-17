from aiogram import Dispatcher, Router

from dialogs import register_dialogs
from .admin import admin_router
from .user import user_router


def register_handlers(dp: Dispatcher):
	dialogs_router = Router()
	register_dialogs(dp, dialogs_router)

	dp.include_routers(
		user_router,
		admin_router,
		dialogs_router  # last
	)
