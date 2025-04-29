from aiogram import Router, types
from aiogram_dialog import DialogManager, ShowMode, StartMode

from filters import LocalizedTextFilter
from state_machines.account import AccountActions

account_router = Router()


@account_router.message(LocalizedTextFilter("btn-profile"), flags={'drop_cache': True})
async def open_profile_h(_: types.Message, dialog_manager: DialogManager):
	# Remember to drop_cache before start dialog
	await dialog_manager.start(AccountActions.ACCOUNT_PANEL, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)
