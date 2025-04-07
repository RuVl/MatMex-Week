from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import get_promocode_by_code, activate_promocode, get_user_by_telegram_id
from keyboards import get_menu_keyboard, get_cancel_keyboard
from state_machines.states_promocode import PromocodeActions

promo_router = Router()

@promo_router.message(F.text == 'Ввести Промокод')
async def promocode_button_pressed(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	await message.answer(
		l10n.format_value("promocode_enter"),
		reply_markup=get_cancel_keyboard()
	)
	await state.set_state(PromocodeActions.ENTER_PROMOCODE)


@promo_router.message(PromocodeActions.ENTER_PROMOCODE, F.text == "Отмена")
async def cancel_help(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	await message.answer(l10n.format_value("cancel_message"),
						 reply_markup=get_menu_keyboard())
	await state.clear()


@promo_router.message(PromocodeActions.ENTER_PROMOCODE)
async def promocode_input(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	user_promocode = message.text
	telegram_id = message.from_user.id

	async with async_session() as session:
		promocode = await get_promocode_by_code(session, user_promocode)
		user = await get_user_by_telegram_id(session, telegram_id)
		is_active = await activate_promocode(session, promocode.id, user.id)

	if is_active:
		await message.answer(l10n.format_value("good-promo-message"),
							 reply_markup=get_menu_keyboard())
	else:
		await message.answer(l10n.format_value("sad-promo-message"),
							 reply_markup=get_menu_keyboard())

	await state.clear()

