from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

code_router = Router()
@code_router.message(F.text == 'Мой код')
async def code_button_pressed(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	#TODO научиться выдавать код
	await message.answer(
		l10n.format_value("sad_code_message")
	)