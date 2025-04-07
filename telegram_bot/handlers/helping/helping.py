from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from keyboards import get_menu_keyboard, get_cancel_keyboard
from state_machines.states_help import HelpActions

help_router = Router()


@help_router.message(F.text == 'Поддержка')
async def help_button_pressed(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	await message.answer(
		l10n.format_value("helping"),
		reply_markup=get_cancel_keyboard()
	)
	await state.set_state(HelpActions.MESSAGE_OR_CANCEL)


@help_router.message(HelpActions.MESSAGE_OR_CANCEL, F.text == "Отмена")
async def cancel_help(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	await message.answer(l10n.format_value("cancel_message"),
						 reply_markup=get_menu_keyboard())
	await state.clear()


@help_router.message(HelpActions.MESSAGE_OR_CANCEL)
async def process_help_message(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	# user_question = message.text
	# user_id = message.from_user.id
	# TODO отправить в чат админов
	await message.answer(
		l10n.format_value("send_helping"),
		reply_markup=get_menu_keyboard()
	)
	await state.clear()
