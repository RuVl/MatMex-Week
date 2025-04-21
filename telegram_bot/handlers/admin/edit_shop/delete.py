from aiogram import Router, types
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from database import async_session
from database.methods import get_category_by_id, remove_category_by_id, remove_item_by_id
from filters.main import LocalizedTextFilter
from keyboards.callback_factories import ShopDeleteCategoryFactory, ShopDeleteItemFactory
from keyboards.inline import get_category_ikb, get_item_ikb
from state_machines import EditShopActions

delete_router = Router()


@delete_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-delete-item-or-category"))
async def delete_category_btn_h(msg: types.Message, l10n: FluentLocalization):
	text = l10n.format_value("shop-hello")
	image_from_pc = types.FSInputFile(MEDIA_DIR / "shop_mock.png")
	category_ikb = await get_category_ikb(l10n, True)
	await msg.answer_photo(image_from_pc, caption=text, reply_markup=category_ikb)


@delete_router.callback_query(ShopDeleteItemFactory.filter())
async def choose_category_h(callback: types.CallbackQuery, callback_data: ShopDeleteItemFactory, l10n: FluentLocalization):
	async with async_session() as session:
		if callback_data.can_delete:
			await remove_item_by_id(session, callback_data.item_id)

	async with async_session() as session:
		category = await get_category_by_id(session, callback_data.category_id)

	await callback.bot.edit_message_media(
		media=types.InputMediaPhoto(media=types.FSInputFile(category.image_path), caption=l10n.format_value("ask-for-item-name")),
		reply_markup=get_item_ikb(l10n, category, callback_data.can_delete),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id
	)


@delete_router.callback_query(ShopDeleteCategoryFactory.filter())
async def delete_category_h(callback: types.CallbackQuery, callback_data: ShopDeleteCategoryFactory, l10n: FluentLocalization):
	async with async_session() as session:
		if callback_data.can_delete:
			await remove_category_by_id(session, callback_data.category_id)

	image_from_pc = types.FSInputFile(MEDIA_DIR / "shop_mock.png")
	category_ikb = await get_category_ikb(l10n, callback_data.can_delete)
	await callback.bot.edit_message_media(
		media=types.InputMediaPhoto(media=image_from_pc, caption=l10n.format_value("shop-hello")),
		reply_markup=category_ikb,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id
	)
