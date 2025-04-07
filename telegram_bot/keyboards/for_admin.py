from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_keyboard():
	buttons_data = [
		("Сканер кодов", "code_scanner"),
		("Создание промокода", "profile"),
		("Список промокодов", "help"),
		("Выдать права", "schedule"),
		("В меню", "schedule"),
	]

	buttons = [
		KeyboardButton(text=text, callback_data=callback_data)
		for text, callback_data in buttons_data
	]

	keyboard = ReplyKeyboardMarkup(keyboard=[
		buttons[:1],
		buttons[1:3],
		buttons[3:4],
		buttons[4:]
	], resize_keyboard=True, input_field_placeholder="Выберите элемент меню")

	return keyboard
