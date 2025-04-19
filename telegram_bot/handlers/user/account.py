from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.methods import get_user_by_telegram_id, update_user_fullname
from filters import FullNameFilter, LocalizedTextFilter
from keyboards.common import menu_kb, account_menu_kb, cancel_kb
from state_machines.account import AccountActions

account_router = Router()


@account_router.message(LocalizedTextFilter("btn-profile"))
async def handle_profile_open(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-profile-action", action="open_profile")

	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		await msg.answer(l10n.format_value("welcome-account", args={
			'fullname': user.full_name,
			'balance': user.balance
		}), reply_markup=account_menu_kb(l10n))

		# TODO добавить купленные товары
		await state.set_state(AccountActions.ACCOUNT_PANEL)
		await log.adebug("log-state-changed", state=AccountActions.ACCOUNT_PANEL.state)


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-edit-name"))
async def handle_edit_name_request(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-profile-action", action="edit_name_started")
	await msg.answer(l10n.format_value("input-new-name"), reply_markup=cancel_kb(l10n))
	await state.set_state(AccountActions.NAME_WAITING)


@account_router.message(AccountActions.NAME_WAITING, LocalizedTextFilter("btn-cancel"))
async def handle_edit_name_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	log.info("log-profile-action", action="edit_name_cancelled")
	await msg.answer(l10n.format_value("cancel-change-name"), reply_markup=account_menu_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)


@account_router.message(AccountActions.NAME_WAITING, FullNameFilter())
async def handle_edit_name_submit(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-profile-action", action="edit_name_submitted")
	await log.adebug("log-name-changed", new_name=msg.text.strip())

	new_name = msg.text.strip()

	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		if user:
			await update_user_fullname(session, user.id, new_name)
			await log.adebug("log-user-data-updated", field="full_name", value=new_name)
		else:
			await log.aerror("user-not-found", telegram_id=msg.from_user.id)

	await msg.answer(l10n.format_value("name-changed", args={
		'fullname': new_name
	}), reply_markup=account_menu_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)


@account_router.message(AccountActions.NAME_WAITING)
async def handle_edit_name_invalid(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	log.info("log-profile-action", action="invalid_name_format", text=msg.text)
	await msg.answer(l10n.format_value("wrong-name"), reply_markup=cancel_kb(l10n))


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-already-in-pc"))
async def handle_already_in_pc(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	log.info("log-profile-action", action="already_in_pc_claimed")
	await msg.answer(l10n.format_value("already-in-pc"), reply_markup=account_menu_kb(l10n))


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-back-to-menu"))
async def handle_back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	log.info("log-profile-action", action="back_to_menu")
	menu = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=menu)
	await state.clear()
