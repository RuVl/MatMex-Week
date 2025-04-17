from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-edit-shop")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-give-rights")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back-to-menu")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-create-promo"))
	)

	return builder.as_markup(resize_keyboard=True)


def edit_item_kb(l10n):
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-category")),
		KeyboardButton(text=l10n.format_value("btn-del-item")),
		KeyboardButton(text=l10n.format_value("btn-back"))
	)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-menu"))


def edit_shop_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-category")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-item")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-edit-item")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-del-item")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back")),
	)

	return builder.as_markup(resize_keyboard=True)
