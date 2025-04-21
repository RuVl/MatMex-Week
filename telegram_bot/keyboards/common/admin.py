from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(KeyboardButton(text=l10n.format_value("btn-give-event-privileges"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-edit-shop"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-edit-events"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-give-rights"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-create-promo"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-back-to-menu")))

	return builder.as_markup(resize_keyboard=True)


def edit_shop_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(KeyboardButton(text=l10n.format_value("btn-add-category"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-add-item"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-delete-item-or-category"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-back")))

	return builder.as_markup(resize_keyboard=True)


def edit_events_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(KeyboardButton(text=l10n.format_value("btn-add-event"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-delete-event"))) \
		.row(KeyboardButton(text=l10n.format_value("btn-back")))

	return builder.as_markup(resize_keyboard=True)
