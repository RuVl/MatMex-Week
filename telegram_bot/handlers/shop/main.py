from aiogram import F
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from keyboards import get_category_keyboard, get_menu_keyboard
from state_machines.states_purchases import PurchasesActions

shop_router = Router()


@shop_router.message(F.text == 'Магазин')
async def schedule_button_pressed(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	text = l10n.format_value("shop_hello")

	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	await message.answer_photo(
		image_from_pc,
		caption=text,
		parse_mode=ParseMode.HTML,
		reply_markup=get_category_keyboard()
	)
	await state.set_state(PurchasesActions.CHOOSE_CATEGORY)


@shop_router.message(PurchasesActions.CHOOSE_CATEGORY, F.text == 'Отмена')
async def schedule_button_pressed(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	text = l10n.format_value("cancel_message")

	await message.answer(
		text,
		reply_markup=get_menu_keyboard()
	)
	await state.clear()


@shop_router.message(PurchasesActions.CHOOSE_CATEGORY, or_f('Шопперы' == F.text, 'Футболки' == F.text))
async def shirts_button_pressed(message: types.Message, state: FSMContext, l10n: FluentLocalization):
	# todo сделать select-запрос и выяснить какие футболки есть и сколько
	shirts_types = ['Матмех', 'Изоклины', 'Тетрис']  # todo select

	await message.answer(l10n.format_value("shirts-type") + str(shirts_types))
	#todo сделать новое состояние с новой клавой и отменой
	await state.set_state(PurchasesActions.CHOOSE_PRODUCT)
