from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.enums import ApplyStatus
from database.methods import get_user_apply, update_user_fullname
from database.models import User
from filters import FullNameFilter, LocalizedTextFilter
from keyboards.common import account_menu_kb, cancel_kb, manual_check_kb, menu_kb
from state_machines.account import AccountActions
from state_machines.registration import RegistrationsActions
from utils import escape_md_v2

account_router = Router()


@account_router.message(LocalizedTextFilter("btn-profile"), flags={'drop_cache': True})
async def profile_open_h(msg: types.Message, state: FSMContext, cached_user: User, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("welcome-account", args={
		'fullname': escape_md_v2(cached_user.full_name),
		'balance': cached_user.balance,
		'in_pc': cached_user.apply is not None and cached_user.apply.status,
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
async def edit_name_submit_h(msg: types.Message, state: FSMContext, cached_user: User, l10n: FluentLocalization, log: FilteringBoundLogger):
	new_name = msg.text.strip()

	await log.adebug("log-name-changed", new_name=new_name)
	async with async_session() as session:
		await update_user_fullname(session, cached_user.id, new_name)

	await msg.answer(l10n.format_value("name-changed", args={'fullname': escape_md_v2(new_name)}), reply_markup=account_menu_kb(l10n))
	await state.set_state(AccountActions.ACCOUNT_PANEL)


@account_router.message(AccountActions.NAME_WAITING)
async def edit_name_invalid_h(msg: types.Message, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("wrong-name"), reply_markup=cancel_kb(l10n))


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-already-in-pc"))
async def already_in_pc_h(msg: types.Message, state: FSMContext, cached_user: User, l10n: FluentLocalization):
	async with async_session() as session:
		apply = await get_user_apply(session, cached_user.id)
	if not apply or apply.status == ApplyStatus.REJECTED:
		await msg.answer(l10n.format_value("ask-pc-profile"), reply_markup=manual_check_kb(l10n))
		await state.set_state(RegistrationsActions.MANUAL_MEMBER_CHECK)
	if apply.status == ApplyStatus.APPROVED:
		await msg.answer(l10n.format_value("already-in-pc"), reply_markup=account_menu_kb(l10n))
	elif apply.status == ApplyStatus.PENDING:
		await msg.answer(l10n.format_value("apply-on-check"), reply_markup=account_menu_kb(l10n))


@account_router.message(AccountActions.ACCOUNT_PANEL, LocalizedTextFilter("btn-back-to-menu"))
async def back_to_menu_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	kb = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=kb)
	await state.clear()
