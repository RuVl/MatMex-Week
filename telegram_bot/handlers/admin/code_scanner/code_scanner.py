from aiogram import F
from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.methods import create_promocode, get_promocode_by_code, get_user_by_telegram_id
from filters import LocalizedTextFilter, AdminPromocodeCreatingFilter
from keyboards.common import admin_kb, cancel_kb, yes_no_kb, get_account_menu_kb, menu_kb
from state_machines import AccrualOfPointsActions, AdminActions
from state_machines import PromocodeActions

code_scanner_router = Router()
code_scanner_router.message.filter(
	F.text  # todo добавить чек на права из базы данных
)


@code_scanner_router.message(LocalizedTextFilter("btn-create-promo"))
async def ask_for_promocode(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-promo-for-creating"), reply_markup=cancel_kb(l10n))
	await state.set_state(PromocodeActions.ENTER_PROMOCODE)

@code_scanner_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-yes"))
async def ask_about_attending_cost(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-cost-promocode"), reply_markup=types.ReplyKeyboardRemove())
	await state.set_state(PromocodeActions.ASK_FOR_COST)

@code_scanner_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-no"))
async def ask_for_promocode_with_no(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-promo-for-creating"), reply_markup=cancel_kb(l10n))

@code_scanner_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-cancel"))
async def back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)

@code_scanner_router.message(PromocodeActions.ASK_FOR_COST)
async def ask_about_cost(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	if not await AdminPromocodeCreatingFilter().__call__(msg):
		await msg.answer(l10n.format_value("wrong-cost"))
		return
	await state.update_data(cost_of_code = int(msg.text))
	await msg.answer(l10n.format_value("ask-for-max-uses"))
	await state.set_state(PromocodeActions.ASK_FOR_MAX_USAGES)

@code_scanner_router.message(PromocodeActions.ASK_FOR_MAX_USAGES)
async def ask_about_usages(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	if not await AdminPromocodeCreatingFilter().__call__(msg):
		await msg.answer(l10n.format_value("wrong-usages"))
		return
	async with async_session() as session:
		state_data = await state.get_data()
		max_usages = int(msg.text)
		user_id = (await get_user_by_telegram_id(session, msg.from_user.id)).id

		#todo data of expiring
		await create_promocode(session, state_data.get("name_of_code"), state_data.get("cost_of_code"), user_id, max_usages, None)
	await msg.answer(l10n.format_value("promo_added"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)

@code_scanner_router.message(PromocodeActions.ENTER_PROMOCODE)
async def ask_about_attending(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	async with async_session() as session:
		code = await get_promocode_by_code(session, msg.text)
		if code is not None:
			await msg.answer(l10n.format_value("promo_exist"))
			return
	await state.update_data(name_of_code = msg.text)
	await msg.answer(l10n.format_value("ask-for-attend-promocode"), reply_markup=yes_no_kb(l10n))






