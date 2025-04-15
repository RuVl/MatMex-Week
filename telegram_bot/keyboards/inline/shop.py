from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import async_session
from database.methods import get_all_categories
from database.models import MerchCategory
from .main import ShopCategoryFactory, ShopItemFactory

async def get_category_ikb(l10n) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	async with async_session() as session:
		categories = await get_all_categories(session)
	for category in categories:
		builder.row(
			InlineKeyboardButton(text=category.name, callback_data=ShopCategoryFactory(category_id = category.id).pack()),
		)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-category"))


def get_item_ikb(l10n, category: MerchCategory) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for item in category.merch_items:
		builder.row(
			InlineKeyboardButton(text=item.name, callback_data=ShopItemFactory(category_id = category.id, item_id = item.id).pack()),
		)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-item"))
