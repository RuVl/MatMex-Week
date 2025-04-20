from aiogram import Router, types
from aiogram.types import FSInputFile, InputMediaPhoto
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from database import async_session
from database.methods import get_category_by_id, get_item_by_id
from filters import LocalizedTextFilter
from keyboards.callback_factories import ShopBackToCategoriesFactory, ShopCategoryFactory, ShopItemFactory
from keyboards.inline import get_back_to_item_ikb, get_category_ikb, get_item_ikb
from utils import escape_md_v2

shop_router = Router()


@shop_router.message(LocalizedTextFilter("btn-shop"))
async def handle_shop_button(msg: types.Message, l10n: FluentLocalization):
	text = l10n.format_value("shop-hello")
	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	kb = await get_category_ikb(l10n, False)
	await msg.answer_photo(
		image_from_pc,
		caption=text,
		reply_markup=kb
	)


@shop_router.callback_query(ShopCategoryFactory.filter())
async def handle_choose_category(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = ShopCategoryFactory.unpack(callback.data)
	async with async_session() as session:
		category = await get_category_by_id(session, data.category_id)

	await callback.bot.edit_message_media(
		media=InputMediaPhoto(media=FSInputFile(category.image_path), caption=l10n.format_value("ask-for-item-name")),
		reply_markup=get_item_ikb(l10n, category, data.can_delete),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id
	)


@shop_router.callback_query(ShopBackToCategoriesFactory.filter())
async def handle_back_to_categories(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = ShopBackToCategoriesFactory.unpack(callback.data)
	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	category_ikb = await get_category_ikb(l10n, data.can_delete)
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(media=image_from_pc, caption=l10n.format_value("shop-hello")),
		reply_markup=category_ikb,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id
	)


@shop_router.callback_query(ShopItemFactory.filter())
async def handle_choose_item(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = ShopItemFactory.unpack(callback.data)
	async with async_session() as session:
		item = await get_item_by_id(session, data.item_id)
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(media=FSInputFile(item.image_path),
                        caption=l10n.format_value("item-value",  args={
                            'itemname': escape_md_v2(item.name),
                            'itemsize': item.size,
                            'fullprice': item.full_price,
                            'discountprice': item.discount_price,
                            'availablecount': item.available_count
                        })),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
		reply_markup=get_back_to_item_ikb(l10n, item, data.can_delete)
	)
