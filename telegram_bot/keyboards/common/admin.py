from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-edit-shop")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-edit-events")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-give-rights")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-create-promo"))
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back-to-menu")),
	)

	return builder.as_markup(resize_keyboard=True)


def edit_shop_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-category")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-item")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-delete-item-or-category")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back")),
	)

	return builder.as_markup(resize_keyboard=True)

def edit_events_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-event")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back")),
	)

	return builder.as_markup(resize_keyboard=True)