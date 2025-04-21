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
async def shop_button_h(msg: types.Message, l10n: FluentLocalization):
	text = l10n.format_value("shop-hello")
	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.png")
	kb = await get_category_ikb(l10n, False)
	await msg.answer_photo(
		image_from_pc,
		caption=text,
		reply_markup=kb
	)


@shop_router.callback_query(ShopCategoryFactory.filter())
async def choose_category_h(callback: types.CallbackQuery, callback_data: ShopCategoryFactory, l10n: FluentLocalization):
	async with async_session() as session:
		category = await get_category_by_id(session, callback_data.category_id)

	await callback.bot.edit_message_media(
		media=InputMediaPhoto(media=FSInputFile(category.image_path), caption=l10n.format_value("ask-for-item-name")),
		reply_markup=get_item_ikb(l10n, category, callback_data.can_delete),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id
	)


@shop_router.callback_query(ShopBackToCategoriesFactory.filter())
async def back_to_categories_h(callback: types.CallbackQuery, callback_data: ShopBackToCategoriesFactory, l10n: FluentLocalization):
	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.png")
	category_ikb = await get_category_ikb(l10n, callback_data.can_delete)
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(media=image_from_pc, caption=l10n.format_value("shop-hello")),
		reply_markup=category_ikb,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id
	)


@shop_router.callback_query(ShopItemFactory.filter())
async def choose_item_h(callback: types.CallbackQuery, callback_data: ShopItemFactory, l10n: FluentLocalization):
	async with async_session() as session:
		item = await get_item_by_id(session, callback_data.item_id)
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(media=FSInputFile(item.image_path),
			caption=l10n.format_value("item-value", args={
				'item_name': escape_md_v2(item.name),
				'item_size': item.size,
				'full_price': item.full_price,
				'discount_price': item.discount_price,
				'available_count': item.available_count
			})),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
		reply_markup=get_back_to_item_ikb(l10n, item, callback_data.can_delete)
	)
