from aiogram import F
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from config import MEDIA_DIR
from keyboards.common import get_category_kb, get_menu_kb, get_item_kb
from state_machines.states_purchases import PurchasesActions
from filters import LocalizedTextFilter
from database import async_session
from database.methods import get_category, get_item
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

@shop_router.message(
	or_f(PurchasesActions.CHOOSE_ITEM, PurchasesActions.CHOOSE_CATEGORY),
	or_f(LocalizedTextFilter("btn-cancel"), LocalizedTextFilter("btn-back"))
)
async def handle_back(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_category")
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=get_menu_kb(l10n))
	await state.clear()

@shop_router.message(PurchasesActions.CHOOSE_CATEGORY)
async def handle_delete_item_choose_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_item_choose_category")
	async with async_session() as session:
		category = await get_category(session, msg.text)
	if not category:
		category_kb = await get_category_kb(l10n)
		await msg.answer(l10n.format_value("category-not-exists"), reply_markup=category_kb)
		return
	await msg.answer_photo(photo = FSInputFile(category.image_path), 
                 caption = l10n.format_value("ask-for-item-name"), 
                 reply_markup=get_item_kb(l10n, category))
	await state.update_data(category_name = category.name)
	await state.set_state(PurchasesActions.CHOOSE_ITEM)
	await log.adebug("log-state-changed", state=PurchasesActions.CHOOSE_ITEM.state)

@shop_router.message(PurchasesActions.CHOOSE_ITEM)
async def handle_delete_item(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_item_btn")
	async with async_session() as session:
		item = await get_item(session, msg.text)
	if not item:
		data = await state.get_data()
		category = await get_category(session, data.get("category_name"))
		category_kb = await get_item_kb(l10n, category)
		await msg.answer(l10n.format_value("item-not-exists"), reply_markup=get_item_kb(l10n, category_kb))
		return
	#TODO: markdownv2 точки
	item_chars = (
		f"Название: {item.name}\n"
		f"Размер: {item.size}\n"
		f"Полная цена: {int(item.full_price)}\n"
		f"Цена со скидкой: {int(item.discount_price)}\n"
		f"На складе: {item.available_count}\n"
		f"{'В наличии' if item.in_stock else 'Пока не продается'}"
	)
	await msg.answer_photo(caption = item_chars, 
                        photo=FSInputFile(item.image_path),
                        reply_markup=get_menu_kb(l10n))
	await state.clear()
	await log.adebug("log-state-changed", state="cleared")