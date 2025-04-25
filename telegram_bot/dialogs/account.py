from aiogram import types
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format

from database import async_session
from database.enums import ApplyStatus
from database.methods import get_user_apply, update_user_fullname
from filters import FullNameFilter
from keyboards.common import manual_check_kb, menu_kb
from state_machines.account import AccountActions
from state_machines.registration import RegistrationsActions
from utils import escape_md_v2


# Helper functions for dialogs
async def get_account_data(dialog_manager: DialogManager, **kwargs):
	cached_user = dialog_manager.middleware_data.get("cached_user")
	l10n = dialog_manager.middleware_data.get("l10n")

	# Format the account welcome message here to avoid Format widget issues
	welcome_text = l10n.format_value("welcome-account", args={
		'fullname': escape_md_v2(cached_user.full_name),
		'balance': cached_user.balance,
		'in_pc': cached_user.apply is not None and cached_user.apply.status,
	})

	input_name_text = l10n.format_value("input-new-name")

	return {
		"fullname": escape_md_v2(cached_user.full_name),
		"balance": cached_user.balance,
		"in_pc": cached_user.apply is not None and cached_user.apply.status,
		"l10n": l10n,
		"welcome_text": welcome_text,
		"input_name_text": input_name_text,
		# Button texts
		"edit_name_btn": l10n.format_value("btn-edit-name"),
		"in_pc_btn": l10n.format_value("btn-already-in-pc"),
		"back_btn": l10n.format_value("btn-back-to-menu"),
		"cancel_btn": l10n.format_value("btn-back-to-menu"),
		"profile_title": "📊 Профиль",
	}


async def edit_name_process(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
	cached_user = dialog_manager.middleware_data.get("cached_user")
	l10n = dialog_manager.middleware_data.get("l10n")
	log = dialog_manager.middleware_data.get("log")

	if not await FullNameFilter().__call__(message):
		await message.answer(l10n.format_value("wrong-name"))
		return

	new_name = message.text.strip()

	await log.adebug("log-name-changed", new_name=new_name)
	async with async_session() as session:
		await update_user_fullname(session, cached_user.id, new_name)

	await message.answer(l10n.format_value("name-changed", args={'fullname': escape_md_v2(new_name)}))

	# Get updated welcome text
	welcome_text = l10n.format_value("welcome-account", args={
		'fullname': escape_md_v2(new_name),
		'balance': cached_user.balance,
		'in_pc': cached_user.apply is not None and cached_user.apply.status,
	})

	await dialog_manager.update({
		"fullname": escape_md_v2(new_name),
		"welcome_text": welcome_text,
	})

	# Return to account panel
	await dialog_manager.switch_to(AccountActions.ACCOUNT_PANEL)


async def check_pc_status(callback: types.CallbackQuery,
                          button: Button, dialog_manager: DialogManager):
	cached_user = dialog_manager.middleware_data.get("cached_user")
	l10n = dialog_manager.middleware_data.get("l10n")
	state = dialog_manager.middleware_data.get("state")

	async with async_session() as session:
		apply = await get_user_apply(session, cached_user.id)

	await dialog_manager.done()

	if not apply or apply.status == ApplyStatus.REJECTED:
		await callback.message.answer(l10n.format_value("ask-pc-profile"), reply_markup=manual_check_kb(l10n))
		await state.set_state(RegistrationsActions.MANUAL_MEMBER_CHECK)
	elif apply.status == ApplyStatus.APPROVED:
		await callback.message.answer(l10n.format_value("already-in-pc"))
		await dialog_manager.start(AccountActions.ACCOUNT_PANEL)
	elif apply.status == ApplyStatus.PENDING:
		await callback.message.answer(l10n.format_value("apply-on-check"))
		await dialog_manager.start(AccountActions.ACCOUNT_PANEL)


async def back_to_main_menu(callback: types.CallbackQuery,
                            button: Button, dialog_manager: DialogManager):
	l10n = dialog_manager.middleware_data.get("l10n")
	kb = await menu_kb(l10n, callback.from_user.id)
	await callback.message.answer(l10n.format_value("back-to-menu"), reply_markup=kb)
	await dialog_manager.done()


async def on_cancel(callback: types.CallbackQuery, button: Button,
                    dialog_manager: DialogManager):
	l10n = dialog_manager.middleware_data.get("l10n")
	await callback.message.answer(l10n.format_value("cancel-change-name"))
	await dialog_manager.switch_to(AccountActions.ACCOUNT_PANEL)


# Dialog windows
account_dialog = Dialog(
	Window(
		Format("{profile_title}"),  # Title from getter
		Format("{welcome_text}"),  # Use pre-formatted text from getter
		Row(
			Button(
				Format("✏️ {edit_name_btn}"),  # Use localized button text
				id="edit_name",
				on_click=lambda c, b, dm: dm.switch_to(AccountActions.NAME_WAITING)
			),
		),
		Row(
			Button(
				Format("👥 {in_pc_btn}"),  # Use localized button text 
				id="check_pc_status",
				on_click=check_pc_status
			),
		),
		Row(
			Button(
				Format("🔙 {back_btn}"),  # Use localized button text
				id="back_to_menu",
				on_click=back_to_main_menu
			),
		),
		state=AccountActions.ACCOUNT_PANEL,
		getter=get_account_data,
	),
	Window(
		Format("{input_name_text}"),
		MessageInput(edit_name_process),
		Cancel(Format("❌ {cancel_btn}")),  # Use localized cancel button
		state=AccountActions.NAME_WAITING,
		getter=get_account_data,
	),
)
