from aiogram import Router, types
from aiogram_dialog import DialogManager, ShowMode, StartMode

from database.models import User
from filters import LocalizedTextFilter
from state_machines.account import AccountActions

account_router = Router()


@account_router.message(LocalizedTextFilter("btn-profile"))
async def open_profile_h(_: types.Message, cached_user: User, dialog_manager: DialogManager):
	await dialog_manager.start(
		AccountActions.ACCOUNT_PANEL,
		data={
			'fullname': cached_user.full_name,
			'balance': cached_user.balance,
			'apply_status': cached_user.apply and cached_user.apply.status
		},
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)
