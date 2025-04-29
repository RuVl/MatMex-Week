from typing import Any

from aiogram import F, types
from aiogram.dispatcher.flags import extract_flags
from aiogram.fsm.context import FSMContext
from aiogram_dialog import Dialog, DialogManager, LaunchMode, ShowMode, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Next, Row
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.enums import ApplyStatus
from database.methods import get_user_apply, get_user_by_telegram_id, update_user_fullname
from database.models import User
from filters import FullNameFilter
from keyboards.common import manual_check_kb
from middlewares import L10N_FORMAT_KEY, LOGGING_KEY, USER_CACHE_KEY
from state_machines import AccountActions, RegistrationsActions
from utils import escape_md_v2
from utils.l10n_format import L10nFormat


async def get_account_data(dialog_manager: DialogManager, **_) -> dict[str, Any]:
	log: FilteringBoundLogger = dialog_manager.middleware_data.get(LOGGING_KEY)

	if dialog_manager.dialog_data.pop('drop_cache', False):
		# Drop cache on next event
		flags = extract_flags(dialog_manager.middleware_data)
		flags['drop_cache'] = True

		await log.adebug('Use db instead cache')
		async with async_session() as session:
			user = await get_user_by_telegram_id(session, dialog_manager.event.from_user.id)
	else:
		user: User = dialog_manager.middleware_data.get(USER_CACHE_KEY)

	return {
		"fullname": escape_md_v2(user.full_name),
		"balance": user.balance,
		"apply_status": getattr(user.apply, 'status', None),
	}


def validate_fullname(name: str) -> str:
	name = name.strip()
	pattern = FullNameFilter().pattern

	if not pattern.match(name):
		raise ValueError('Invalid fullname')
	return name


async def edit_name_h(_: types.Message, __: TextInput, dialog_manager: DialogManager, fullname: str):
	cached_user = dialog_manager.middleware_data.get(USER_CACHE_KEY)
	log: FilteringBoundLogger = dialog_manager.middleware_data.get(LOGGING_KEY)

	await log.adebug("log-name-changed", new_name=fullname)
	async with async_session() as session:
		await update_user_fullname(session, cached_user.id, fullname)

	# Update cache
	dialog_manager.dialog_data.update(drop_cache=True)
	await dialog_manager.back(ShowMode.EDIT)


async def wrong_name_h(message: types.Message, _: MessageInput, dialog_manager: DialogManager, error: ValueError):
	l10n = dialog_manager.middleware_data.get(L10N_FORMAT_KEY)
	log = dialog_manager.middleware_data.get(LOGGING_KEY)

	await log.adebug("log-name-validate-error", error=str(error))
	await message.answer(l10n.format_value("wrong-name"))

	# Do not resend the window
	await dialog_manager.switch_to(AccountActions.NAME_WAITING, ShowMode.EDIT)


async def check_pc_status_h(callback: types.CallbackQuery, _: Button, dialog_manager: DialogManager):
	cached_user: User = dialog_manager.middleware_data.get(USER_CACHE_KEY)
	l10n: FluentLocalization = dialog_manager.middleware_data.get(L10N_FORMAT_KEY)
	log: FilteringBoundLogger = dialog_manager.middleware_data.get(LOGGING_KEY)
	state: FSMContext = dialog_manager.middleware_data.get("state")

	await log.adebug("check-pc-apply-status")
	async with async_session() as session:
		apply = await get_user_apply(session, cached_user.id)

	# Update cache on next event
	dialog_manager.dialog_data.update(drop_cache=True)

	if apply is None:
		await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
		await state.set_state(RegistrationsActions.MANUAL_MEMBER_CHECK)
		await callback.message.answer(l10n.format_value("ask-pc-profile"), reply_markup=manual_check_kb(l10n))
		return

	match apply.status:
		case ApplyStatus.REJECTED:
			await callback.answer(l10n.format_value("apply-rejected-clb"))
		case ApplyStatus.APPROVED:
			await callback.answer(l10n.format_value("apply-approved-clb"))
		case ApplyStatus.PENDING:
			await callback.answer(l10n.format_value("apply-on-check-clb"))

	await dialog_manager.show(ShowMode.EDIT)


account_dialog = Dialog(
	Window(
		L10nFormat("profile-title"),
		L10nFormat("welcome-account", args={
			"fullname": "{fullname}",
			"balance": "{balance}",
			"apply_status": "{apply_status}",
		}),
		Row(
			Next(L10nFormat("btn-edit-name"), "edit_name"),
		),
		Row(
			Button(L10nFormat("btn-already-in-pc", args={
				"apply_status": "{apply_status}",
			}), "check_pc_status", check_pc_status_h, when=F['apply_status'] != ApplyStatus.APPROVED),
		),
		Row(
			Cancel(L10nFormat("btn-back-to-menu"), "back2menu"),
		),
		state=AccountActions.ACCOUNT_PANEL,
		getter=get_account_data,
	),
	Window(
		L10nFormat("input-new-name"),
		TextInput('name_waiting', validate_fullname, edit_name_h, wrong_name_h),
		Back(L10nFormat("btn-cancel"), 'back2profile', show_mode=ShowMode.EDIT),
		state=AccountActions.NAME_WAITING,
	),
	launch_mode=LaunchMode.SINGLE_TOP,
)
