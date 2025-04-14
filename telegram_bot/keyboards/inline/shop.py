from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import async_session
from database.methods import get_all_categories
from database.models import MerchCategory, MerchItem
from .main import ShopCategoryFactory, ShopItemFactory, ShopDeleteItemFactory, ShopDeleteCategoryFactory, ShopBackToCategoriesFactory

async def get_category_ikb(l10n, can_delete : bool) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	async with async_session() as session:
		categories = await get_all_categories(session)
	for category in categories:
		builder.row(
			InlineKeyboardButton(text=category.name, callback_data=ShopCategoryFactory(category_id = category.id, can_delete=can_delete).pack()),
		)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-category"))


def get_item_ikb(l10n, category: MerchCategory, can_delete : bool) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for item in category.merch_items:
		builder.row(
			InlineKeyboardButton(text=item.name, callback_data=ShopItemFactory(category_id = category.id, item_id = item.id, can_delete=can_delete).pack()),
		)
	if can_delete:
		builder.row(InlineKeyboardButton(
									text=l10n.format_value("btn-delete-category"), 
									callback_data=ShopDeleteCategoryFactory(category_id=category.id, can_delete=can_delete).pack()))
	builder.row(InlineKeyboardButton(
    								text=l10n.format_value("btn-back"), 
     								callback_data=ShopBackToCategoriesFactory(can_delete=can_delete).pack()))
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-item"))

def get_back_to_item_ikb(l10n, item: MerchItem, can_delete : bool) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	if can_delete:
		builder.row(InlineKeyboardButton(
									text=l10n.format_value("btn-delete-item"), 
									callback_data=ShopDeleteItemFactory(category_id = item.category_id, item_id = item.id, can_delete=can_delete).pack()))
	builder.row(InlineKeyboardButton(
     								text=l10n.format_value("btn-back"), 
             						callback_data=ShopCategoryFactory(category_id = item.category_id, can_delete=can_delete).pack()))
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-get-back-to-item"))