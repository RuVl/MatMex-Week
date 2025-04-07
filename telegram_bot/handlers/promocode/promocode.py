from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from state_machines.states_promocode import PromocodeActions
from keyboards import get_menu_keyboard, get_cancel_keyboard

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
	#TODO отослать промокод на проверку в бд
	#is_active = ... if is_active:
	await message.answer(l10n.format_value("sad_promo_message"),
						 reply_markup=get_menu_keyboard())
	await state.clear()

