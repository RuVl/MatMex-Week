from aiogram import F
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from config import MEDIA_DIR
from keyboards.common import get_menu_kb
from keyboards.inline import get_category_ikb, get_item_ikb
from state_machines.states_purchases import PurchasesActions
from filters import LocalizedTextFilter
from database import async_session
from database.methods import get_category_by_id, get_item_by_id
from keyboards.inline import ShopCategoryFactory, ShopItemFactory
shop_router = Router()


@shop_router.message(LocalizedTextFilter("btn-shop"))
async def handle_shop_button(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	text = l10n.format_value("shop_hello")
	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	category_ikb = await get_category_ikb(l10n)
	await msg.answer_photo(
		image_from_pc,
		caption=text,
		parse_mode=ParseMode.HTML,
		reply_markup=category_ikb
	)
	await log.adebug("log-state-changed", state=PurchasesActions.CHOOSE_CATEGORY.state)

@shop_router.callback_query(ShopCategoryFactory.filter(F))
async def handle_choose_category(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = ShopCategoryFactory.unpack(callback.data)
	async with async_session() as session:
		category = await get_category_by_id(session, data.category_id)
	
	await callback.bot.edit_message_media(
     									media = InputMediaPhoto(media = FSInputFile(category.image_path),
																caption = l10n.format_value("ask-for-item-name")),
              							reply_markup=get_item_ikb(l10n, category),
                                    	chat_id=callback.message.chat.id,
        								message_id=callback.message.message_id)
@shop_router.callback_query(ShopItemFactory.filter(F))
async def handle_choose_item(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = ShopItemFactory.unpack(callback.data)
	async with async_session() as session:
		item = await get_item_by_id(session, data.item_id)
	#TODO: markdownv2 точки
	item_chars = (
		f"Название: {item.name}\n"
		f"Размер: {item.size}\n"
		f"Полная цена: {int(item.full_price)}\n"
		f"Цена со скидкой: {int(item.discount_price)}\n"
		f"На складе: {item.available_count}\n"
		f"{'В наличии' if item.in_stock else 'Пока не продается'}"
	)
	await callback.message.answer_photo(
     					caption = item_chars, 
                        photo=FSInputFile(item.image_path),
                        reply_markup=get_menu_kb(l10n))