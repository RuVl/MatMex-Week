from aiogram import Router

from .account import account_dialog

user_dialogs_router = Router()

user_dialogs_router.include_routers(
	account_dialog,
)
