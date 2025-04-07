from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

profile_router = Router()


@profile_router.message(F.text == 'Профиль')
async def profile_button_pressed(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	#TODO научиться выдавать профиль, запрос из Б/Д
	await message.answer(
		l10n.format_value("phrase_profile")
	)