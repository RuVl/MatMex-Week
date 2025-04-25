from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from .admin import admin_router
from .user import user_router


def register_handlers(dp: Dispatcher):
	dp.include_routers(
		user_router,
		admin_router,
	)

	# Setup dialogs
	setup_dialogs(dp)
