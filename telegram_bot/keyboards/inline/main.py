from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def cancel_ikb(l10n):
	builder = InlineKeyboardBuilder()
	builder.row(InlineKeyboardButton(text=l10n.format_value(
		"btn-cancel"), callback_data="btn_cancel"))
	return builder.as_markup(resize_keyboard=True)


def yes_no_cancel_ikb(l10n):
	builder = InlineKeyboardBuilder()
	builder.row(
		InlineKeyboardButton(text=l10n.format_value(
			"btn-yes"), callback_data="btn_yes"),
		InlineKeyboardButton(text=l10n.format_value("btn-no"), callback_data="btn_no"))\
			.row(InlineKeyboardButton(text=l10n.format_value(
		"btn-cancel"), callback_data="btn_cancel"))
	return builder.as_markup(resize_keyboard=True)
