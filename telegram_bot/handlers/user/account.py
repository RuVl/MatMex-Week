from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import get_user_by_telegram_id, update_user_fullname
from filters import FullNameFilter
from handlers.utils import logger, get_user_context, localized_text_filter
from keyboards.common import get_menu_kb, get_account_menu_kb, get_cancel_kb
from state_machines.states_account import AccountActions

account_router = Router()


@account_router.message(F.text.func(localized_text_filter("btn-profile")))
async def handle_profile_open(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_profile_open")
	log.info("log-profile-action", action="open_profile")

	await msg.answer(l10n.format_value("account-temp"), reply_markup=get_account_menu_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)

	log.info("log-state-changed", state=AccountActions.ACCOUNT_PANEL.state)
	log.info("log-handler-completed")


@account_router.message(AccountActions.ACCOUNT_PANEL, F.text.func(localized_text_filter("btn-edit-name")))
async def handle_edit_name_request(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_edit_name_request")
	log.info("log-profile-action", action="edit_name_started")

	await msg.answer(l10n.format_value("input-new-name"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(AccountActions.NAME_WAITING)

	log.info("log-state-changed", state=AccountActions.NAME_WAITING.state)
	log.info("log-handler-completed")


@account_router.message(AccountActions.NAME_WAITING, F.text.func(localized_text_filter("btn-cancel")))
async def handle_edit_name_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_edit_name_cancel")
	log.info("log-profile-action", action="edit_name_cancelled")

	await msg.answer(l10n.format_value("cancel-change-name"), reply_markup=get_account_menu_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)

	log.info("log-state-changed", state=AccountActions.ACCOUNT_PANEL.state)
	log.info("log-handler-completed")


@account_router.message(AccountActions.NAME_WAITING, FullNameFilter())
async def handle_edit_name_submit(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_edit_name_submit")
	log.info("log-name-changed", new_name=msg.text.strip())

	new_name = msg.text.strip()

	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		if user:
			await update_user_fullname(session, user.id, new_name)
			log.info("log-user-data-updated", field="full_name", value=new_name)
		else:
			log.error("user-not-found", telegram_id=msg.from_user.id)

	await msg.answer(l10n.format_value("name-changed") + ", " + new_name + r'\!', reply_markup=get_account_menu_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)

	log.info("log-state-changed", state=AccountActions.ACCOUNT_PANEL.state)
	log.info("log-handler-completed")


@account_router.message(AccountActions.NAME_WAITING)
async def handle_edit_name_invalid(msg: types.Message, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_edit_name_invalid")
	log.info("log-profile-action", action="invalid_name_format", text=msg.text)

	await msg.answer(l10n.format_value("wrong-name"), reply_markup=get_cancel_kb(l10n))

	log.info("log-handler-completed")


@account_router.message(AccountActions.ACCOUNT_PANEL, F.text.func(localized_text_filter("btn-already-in-pc")))
async def handle_already_in_pc(msg: types.Message, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_already_in_pc")
	log.info("log-profile-action", action="already_in_pc_claimed")

	await msg.answer(l10n.format_value("already-in-pc"), reply_markup=get_account_menu_kb(l10n))

	log.info("log-handler-completed")


@account_router.message(AccountActions.ACCOUNT_PANEL, F.text.func(localized_text_filter("btn-back-to-menu")))
async def handle_back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_back_to_menu")
	log.info("log-profile-action", action="back_to_menu")

	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=get_menu_kb(l10n))
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")
