from aiogram import F
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from config import MEDIA_DIR
from keyboards.common import get_category_kb, get_menu_kb
from state_machines.states_purchases import PurchasesActions
from filters import LocalizedTextFilter

shop_router = Router()


@shop_router.message(LocalizedTextFilter("btn-shop"))
async def handle_shop_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	text = l10n.format_value("shop_hello")

	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	category_kb = await get_category_kb(l10n)
	await msg.answer_photo(
		image_from_pc,
		caption=text,
		parse_mode=ParseMode.HTML,
		reply_markup=category_kb
	)
	await state.set_state(PurchasesActions.CHOOSE_CATEGORY)
	await log.adebug("log-state-changed", state=PurchasesActions.CHOOSE_CATEGORY.state)


@shop_router.message(PurchasesActions.CHOOSE_CATEGORY, LocalizedTextFilter("btn-back"))
async def handle_shop_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	text = l10n.format_value("cancel_edit_shop")

	await msg.answer(
		text,
		reply_markup=get_menu_kb(l10n)
	)
	await state.clear()
	await log.adebug("log-state-changed", state="cleared")


@shop_router.message(PurchasesActions.CHOOSE_CATEGORY, or_f(LocalizedTextFilter("btn-tshirts"), 
                                                            LocalizedTextFilter("btn-bracelets"),
                                                            LocalizedTextFilter("btn-id-covers"),
                                                            LocalizedTextFilter("btn-shoppers")))
async def handle_shop_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	# todo сделать select-запрос и выяснить какие футболки есть и сколько
	shirts_types = ['Матмех', 'Изоклины', 'Тетрис']  # todo select

	await msg.answer(l10n.format_value("shirts-type") + str(shirts_types))
	# todo сделать новое состояние с новой клавой и отменой
	await state.set_state(PurchasesActions.CHOOSE_PRODUCT)
	await log.adebug("log-state-changed", state=PurchasesActions.CHOOSE_PRODUCT.state)
