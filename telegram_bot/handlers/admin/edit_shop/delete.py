from aiogram import F
from aiogram import Router, types
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from config import MEDIA_DIR
from database import async_session
from database.methods import remove_item_by_id, remove_category_by_id, get_category_by_id
from filters.main import LocalizedTextFilter
from keyboards.callback_factories import ShopDeleteCategoryFactory, ShopDeleteItemFactory
from keyboards.inline import get_category_ikb, get_item_ikb
from state_machines import EditShopActions

edit_shop_delete_router = Router()


@edit_shop_delete_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-delete-item-or-category"))
async def handle_delete_category_btn(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_category_btn")
	text = l10n.format_value("shop-hello")
	image_from_pc = types.FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	category_ikb = await get_category_ikb(l10n, True)
	await msg.answer_photo(
		image_from_pc,
		caption=text,
		reply_markup=category_ikb
	)
	await log.adebug("log-state-changed", state=EditShopActions.EDIT_SHOP.state)


@edit_shop_delete_router.callback_query(ShopDeleteItemFactory.filter(F))
async def handle_choose_category(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = ShopDeleteItemFactory.unpack(callback.data)
	async with async_session() as session:
		if data.can_delete:
			await remove_item_by_id(session, data.item_id)
	async with async_session() as session:
		category = await get_category_by_id(session, data.category_id)

	await callback.bot.edit_message_media(
		media=types.InputMediaPhoto(media=types.FSInputFile(category.image_path),
		                            caption=l10n.format_value("ask-for-item-name")),
		reply_markup=get_item_ikb(l10n, category, data.can_delete),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id)


@edit_shop_delete_router.callback_query(ShopDeleteCategoryFactory.filter(F))
async def handle_delete_category(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = ShopDeleteCategoryFactory.unpack(callback.data)
	async with async_session() as session:
		if data.can_delete:
			await remove_category_by_id(session, data.category_id)
	image_from_pc = types.FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	category_ikb = await get_category_ikb(l10n, data.can_delete)
	await callback.bot.edit_message_media(
		media=types.InputMediaPhoto(media=image_from_pc,
		                            caption=l10n.format_value("shop-hello")),
		reply_markup=category_ikb,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id)
