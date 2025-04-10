from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_yes_no_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-yes")),
		KeyboardButton(text=l10n.format_value("btn-no")),
	)

	return builder.as_markup(resize_keyboard=True)


def get_account_menu_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-edit-name")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-already-in-pc")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back")),
	)

	return builder.as_markup(resize_keyboard=True)


def manual_check_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-send-for-check"))
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-just-kidding"))
	)

	return builder.as_markup(resize_keyboard=True)


def get_menu_kb(l10n) -> ReplyKeyboardMarkup:
	isAdmin = True  # TODO чек на права из базы данных

	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-support")),
		KeyboardButton(text=l10n.format_value("btn-schedule")),
	).row(
		KeyboardButton(text=l10n.format_value("btn-my-code")),
		KeyboardButton(text=l10n.format_value("btn-enter-promocode")),
	).row(
		KeyboardButton(text=l10n.format_value("btn-profile")),
		KeyboardButton(text=l10n.format_value("btn-shop")),
	)

	if isAdmin:
		builder.row(KeyboardButton(text=l10n.format_value("btn-admin-panel")))

	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-menu"))


def get_category_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-tshirts")),
	).row(
		KeyboardButton(text=l10n.format_value("btn-bracelets")),
	).row(
		KeyboardButton(text=l10n.format_value("btn-id-covers")),
	).row(
		KeyboardButton(text=l10n.format_value("btn-shoppers")),
	).row(
		KeyboardButton(text=l10n.format_value("btn-back")),
	)

	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-category"))
