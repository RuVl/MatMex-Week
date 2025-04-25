from aiogram import Router, types
from aiogram_dialog import DialogManager
from fluent.runtime import FluentLocalization

from database.models import User
from dialogs.account import account_dialog
from filters import LocalizedTextFilter
from state_machines.account import AccountActions

account_router = Router()

# Register dialog with the router
account_router.include_router(account_dialog)


# Standard router handler for entry point
@account_router.message(LocalizedTextFilter("btn-profile"), flags={'drop_cache': True})
async def profile_open_h(msg: types.Message,
                         cached_user: User, dialog_manager: DialogManager,
                         l10n: FluentLocalization):
	await dialog_manager.start(AccountActions.ACCOUNT_PANEL)
