from aiogram.utils.keyboard import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup


def get_yes_no_kb() -> ReplyKeyboardMarkup:
	kb = ReplyKeyboardBuilder()
	kb.row(KeyboardButton(text="Да"),
	       KeyboardButton(text="Нет"))
	return kb.as_markup(resize_keyboard=True)


def manual_check_kb() -> ReplyKeyboardMarkup:
	kb = ReplyKeyboardBuilder()
	kb.row(KeyboardButton(text="Отправить на ручную проверку"),
	       KeyboardButton(text="Нет, я пошутил"))
	return kb.as_markup(resize_keyboard=True)
