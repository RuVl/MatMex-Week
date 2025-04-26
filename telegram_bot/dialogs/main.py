from aiogram import Dispatcher, Router
from aiogram_dialog import setup_dialogs

from dialogs.user import account_dialog


def register_dialogs(dp: Dispatcher, router: Router):
	setup_dialogs(dp)  # Register on dispatcher for using anywhere
	router.include_router(account_dialog)
