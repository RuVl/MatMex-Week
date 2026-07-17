from aiogram import Dispatcher, Router
from aiogram_dialog import setup_dialogs

from dialogs.admin import admin_dialog_router
from dialogs.user import user_dialogs_router


def register_dialogs(dp: Dispatcher, router: Router):
	setup_dialogs(dp)  # Register on dispatcher for using anywhere
	
	router.include_routers(
		user_dialogs_router,
		admin_dialog_router
	)
