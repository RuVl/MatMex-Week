from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database import async_session
from database.methods import get_all_categories, get_privilege_by_user, get_user_by_telegram_id


def get_account_menu_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-edit-name")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-already-in-pc")),
	)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back-to-menu")),
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


async def menu_kb(l10n, user_telegram_id: int) -> ReplyKeyboardMarkup:
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, user_telegram_id)
		user_privilege = await get_privilege_by_user(session, user.id)
	is_admin = True
	if not user_privilege or user_privilege.privilege == 0:
		is_admin = False
	
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

	if is_admin:
		builder.row(KeyboardButton(text=l10n.format_value("btn-admin-panel")))

	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-menu"))


async def category_kb(l10n) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()
	async with async_session() as session:
		categories = await get_all_categories(session)
	for item in categories:
		builder.row(
			KeyboardButton(text=item.name),
		)
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-back")),
	)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-category"))

def user_codes_kb(l10n):
	builder = ReplyKeyboardBuilder()
	builder.row(
		KeyboardButton(text=l10n.format_value("btn-user-codes")),
	).row(
		KeyboardButton(text=l10n.format_value("btn-cancel")),
	)
	return builder.as_markup(resize_keyboard=True)
