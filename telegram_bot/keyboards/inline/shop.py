from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import async_session
from database.enums import MerchSize
from database.methods import get_all_categories
from database.models import MerchCategory, MerchItem
from keyboards.callback_factories import (
	EditShopCategoryFactory, ShopBackToCategoriesFactory, ShopCategoryFactory, ShopDeleteCategoryFactory, ShopDeleteItemFactory, ShopItemFactory,
)


async def get_category_ikb(l10n, can_delete: bool) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	async with async_session() as session:
		categories = await get_all_categories(session)
	for category in categories:
		builder.row(
			InlineKeyboardButton(text=category.name, callback_data=ShopCategoryFactory(
				category_id=category.id, can_delete=can_delete
			).pack()
			),
		)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-category"))


async def get_edit_shop_category_ikb(l10n) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	async with async_session() as session:
		categories = await get_all_categories(session)
	for category in categories:
		builder.row(
			InlineKeyboardButton(text=category.name, callback_data=EditShopCategoryFactory(
				category_id=category.id
			).pack()
			),
		)
	builder.row(
		InlineKeyboardButton(text=l10n.format_value(
			"btn-cancel"
		), callback_data="btn_cancel"
		),
	)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-category"))


def get_item_ikb(l10n, category: MerchCategory, can_delete: bool) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for item in category.merch_items:
		if item.in_stock or can_delete:
			builder.row(
				InlineKeyboardButton(text=item.name, callback_data=ShopItemFactory(
					category_id=category.id, item_id=item.id, can_delete=can_delete
				).pack()
				),
			)
	if can_delete:
		builder.row(InlineKeyboardButton(
			text=l10n.format_value("btn-delete-category"),
			callback_data=ShopDeleteCategoryFactory(category_id=category.id, can_delete=can_delete).pack()
		)
		)
	builder.row(InlineKeyboardButton(
		text=l10n.format_value("btn-back"),
		callback_data=ShopBackToCategoriesFactory(can_delete=can_delete).pack()
	)
	)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-item"))


def get_back_to_item_ikb(l10n, item: MerchItem, can_delete: bool) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	if can_delete:
		builder.row(
			InlineKeyboardButton(text=l10n.format_value("btn-delete-item"),
				callback_data=ShopDeleteItemFactory(category_id=item.category_id, item_id=item.id, can_delete=can_delete).pack()
			)
		)

	builder.row(
		InlineKeyboardButton(text=l10n.format_value("btn-back"),
			callback_data=ShopCategoryFactory(category_id=item.category_id, can_delete=can_delete).pack()
		)
	)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-get-back-to-item"))


def get_item_size_ikb(l10n) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for size in MerchSize:
		builder.row(InlineKeyboardButton(text=size.value, callback_data=size.value))

	builder.row(InlineKeyboardButton(text=l10n.format_value("btn-cancel"), callback_data="btn_cancel"))

	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-item-size"))
