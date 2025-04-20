from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import activate_promocode, get_user_activations, get_user_by_telegram_id
from database.models import User
from filters import LocalizedTextFilter
from keyboards.common import menu_kb, user_codes_kb
from state_machines import PromocodeActions
from utils import escape_md_v2

promocode_router = Router()


@promocode_router.message(LocalizedTextFilter("btn-enter-promocode"))
async def handle_promocode_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("promocode_enter"), reply_markup=user_codes_kb(l10n))
	await state.set_state(PromocodeActions.ENTER_PROMOCODE)


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-cancel"))
async def handle_promocode_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	kb = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("cancel"), reply_markup=kb)
	await state.clear()


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-user-codes"))
async def handle_promocode_list(msg: types.Message):
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		activations = await get_user_activations(session, user.id)

	str_lst = '\n'.join(escape_md_v2(pa.promocode.code) for pa in activations)
	await msg.answer(str_lst)


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE)
async def handle_promocode_input(msg: types.Message, cached_user: User):
	promocode_code = msg.text.strip()

	async with async_session() as session:
		act_promo = await activate_promocode(session, promocode_code, cached_user.id)
		msg_answer = act_promo[1]  # TODO МЕТОДЫ НЕ ДОЛЖНЫ ВОЗВРАЩАТЬ ТЕКСТ ТГ
		await msg.answer(msg_answer)
