from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_kb(l10n):
	keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(
		text=l10n.format_value("btn-cancel"))]], resize_keyboard=True)
	return keyboard


def yes_no_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(KeyboardButton(text=l10n.format_value("btn-yes")),
				KeyboardButton(text=l10n.format_value("btn-no")))
	return builder.as_markup(resize_keyboard=True)


def yes_no_cancel_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(KeyboardButton(text=l10n.format_value("btn-yes")),
				KeyboardButton(text=l10n.format_value("btn-no")))
	builder.row(KeyboardButton(text=l10n.format_value("btn-cancel")))
	return builder.as_markup(resize_keyboard=True)
