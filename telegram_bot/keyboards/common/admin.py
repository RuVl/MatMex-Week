from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from utils import SupportCallback

def get_admin_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-admin-panel")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-edit-shop")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-scan-code")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-custom-prize")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back")),
	)

	return builder.as_markup(resize_keyboard=True)


def get_edit_item_kb(l10n):
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-add-item")),
		KeyboardButton(text=l10n.format_value("btn-del-item")),
		KeyboardButton(text=l10n.format_value("btn-back"))
	)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-menu"))


def get_edit_shop_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
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

def get_send_support_inline_kb(l10n, callback_data : SupportCallback) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	callback_data.command = 'send_support'
	builder.row(
		InlineKeyboardButton(text=l10n.format_value("btn-send-support"), callback_data=callback_data.pack()),
	)

	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-menu"))

def get_cancel_inline_kb(l10n, callback_data : SupportCallback) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	callback_data.command = 'cancel_send_support'
	builder.row(
		InlineKeyboardButton(text=l10n.format_value("btn-cancel-support"), callback_data=callback_data.pack()),
	)

	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-menu"))