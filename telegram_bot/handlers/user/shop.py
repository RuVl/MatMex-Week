from aiogram import Router, types
from aiogram.types import FSInputFile, InputMediaPhoto
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from database import async_session
from database.methods import get_category_by_id, get_item_by_id, get_user_purchases, get_user_by_telegram_id, buy_item
from filters import LocalizedTextFilter
from keyboards.callback_factories import (
	ShopBackToCategoriesFactory,
	ShopCategoryFactory,
	ShopItemFactory,
	IsSureBuyItemFactory,
	BuyItemFactory,
)
from keyboards.inline import item_actions_ikb, get_category_ikb, get_item_ikb, yes_no_buy_ikb
from utils import escape_md_v2

shop_router = Router()


@shop_router.message(LocalizedTextFilter("btn-shop"))
async def shop_button_h(msg: types.Message, l10n: FluentLocalization):
	text = l10n.format_value("shop-hello")  # TODO: вынести в профиль и сделать клавиатурой
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		purchases = await get_user_purchases(session, user.id)
		if purchases:
			text += f"\n{l10n.format_value('purchases')}\n"
			for purchase in user.purchases:
				item = await get_item_by_id(session, purchase.merch_id)
				text += f"{item.full_name()}: {purchase.quantity}\n"
	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.png")
	kb = await get_category_ikb(l10n, False)
	await msg.answer_photo(image_from_pc, caption=text, reply_markup=kb)


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
	text = l10n.format_value("shop-hello")
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, callback.from_user.id)
		purchases = await get_user_purchases(session, user.id)
		if purchases:
			text += f"\n{l10n.format_value('purchases')}\n"
			for purchase in user.purchases:
				item = await get_item_by_id(session, purchase.merch_id)
				text += f"{item.full_name()}: {purchase.quantity}\n"
	category_ikb = await get_category_ikb(l10n, callback_data.can_delete)
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(media=image_from_pc, caption=text),
		reply_markup=category_ikb,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
	)


@shop_router.callback_query(ShopItemFactory.filter())
async def choose_item_h(callback: types.CallbackQuery, callback_data: ShopItemFactory, l10n: FluentLocalization):
	async with async_session() as session:
		item = await get_item_by_id(session, callback_data.item_id)
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(
			media=FSInputFile(item.image_path),
			caption=l10n.format_value(
				"item-value",
				args={
					"item_name": escape_md_v2(item.name),
					"item_size": item.size,
					"full_price": item.full_price,
					"discount_price": item.discount_price,
					"available_count": item.available_count,
				},
			),
		),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
		reply_markup=item_actions_ikb(l10n, item, callback_data.can_delete),
	)


@shop_router.callback_query(IsSureBuyItemFactory.filter())
async def is_sure_buy_item_h(callback: types.CallbackQuery, callback_data: IsSureBuyItemFactory, l10n: FluentLocalization):
	async with async_session() as session:
		item = await get_item_by_id(session, callback_data.item_id)
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(
			media=FSInputFile(item.image_path),
			caption=l10n.format_value(
				"item-value",
				args={
					"item_name": escape_md_v2(item.name),
					"item_size": item.size,
					"full_price": item.full_price,
					"discount_price": item.discount_price,
					"available_count": item.available_count,
					"are_you_sure": True,
				},
			),
		),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
		reply_markup=yes_no_buy_ikb(l10n, item, callback_data.can_delete),
	)


@shop_router.callback_query(BuyItemFactory.filter())
async def buy_item_h(callback: types.CallbackQuery, callback_data: BuyItemFactory, l10n: FluentLocalization):
	async with async_session() as session:
		item = await get_item_by_id(session, callback_data.item_id)
		result_code = await buy_item(session, callback.from_user.id, callback_data.item_id)
	result_mapping = {
		"item_not_in_stock": "item-not-in-stock",
		"too_expensive": "item-too-expensive",
		"successfully_bought": "item-successfully-bought",
	}

	result_key = result_mapping.get(result_code, "item-result-unknown")
	await callback.answer(l10n.format_value(result_key))
	await callback.bot.edit_message_media(
		media=InputMediaPhoto(
			media=FSInputFile(item.image_path),
			caption=l10n.format_value(
				"item-value",
				args={
					"item_name": escape_md_v2(item.name),
					"item_size": item.size,
					"full_price": item.full_price,
					"discount_price": item.discount_price,
					"available_count": item.available_count,
				},
			),
		),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
		reply_markup=item_actions_ikb(l10n, item, callback_data.can_delete),
	)
