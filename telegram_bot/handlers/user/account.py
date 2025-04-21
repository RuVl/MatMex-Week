from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.methods import get_user_by_telegram_id, update_user_fullname
from filters import FullNameFilter, LocalizedTextFilter
from keyboards.common import account_menu_kb, cancel_kb, menu_kb
from state_machines.account import AccountActions

account_router = Router()


@account_router.message(LocalizedTextFilter("btn-profile"))
async def profile_open_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)

	await msg.answer(l10n.format_value("welcome-account", args={
		'fullname': user.full_name,
		'balance': user.balance,
		'in_pc': user.apply is not None,
	}), reply_markup=account_menu_kb(l10n))

	# TODO добавить купленные товары
	await state.set_state(AccountActions.ACCOUNT_PANEL)


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-edit-name"))
async def edit_name_request_h(msg: types.Message, l10n: FluentLocalization, state: FSMContext):
	await msg.answer(l10n.format_value("input-new-name"), reply_markup=account_menu_kb(l10n))
	await state.set_state(AccountActions.NAME_WAITING)


@account_router.message(AccountActions.NAME_WAITING, LocalizedTextFilter("btn-cancel"))
async def edit_name_cancel_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("cancel-change-name"), reply_markup=cancel_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)


@account_router.message(AccountActions.NAME_WAITING, FullNameFilter())
async def edit_name_submit_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-name-changed", new_name=msg.text.strip())
	new_name = msg.text.strip()

	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		if user:
			await update_user_fullname(session, user.id, new_name)
			await log.adebug("log-user-data-updated", field="full_name", value=new_name)
		else:
			await log.aerror("user-not-found", telegram_id=msg.from_user.id)

	await msg.answer(l10n.format_value("name-changed", args={'fullname': new_name}), reply_markup=account_menu_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)


@account_router.message(AccountActions.NAME_WAITING)
async def edit_name_invalid_h(msg: types.Message, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("wrong-name"), reply_markup=cancel_kb(l10n))


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-already-in-pc"))
async def already_in_pc_h(msg: types.Message, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("already-in-pc"), reply_markup=account_menu_kb(l10n))


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-back-to-menu"))
async def back_to_menu_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	menu = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=menu)
	await state.clear()
