from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_edit_shop_keyboard():
	buttons_data = [
		("Добавить категорию", "add_category"),
		("Редактировать категорию", "edit_category"),
		("Назад", "back")
	]

	buttons = [
		KeyboardButton(text=text, callback_data=callback_data)
		for text, callback_data in buttons_data
	]

	keyboard = ReplyKeyboardMarkup(keyboard=[
		buttons[:1],
		buttons[1:2],
		buttons[2:]
	], resize_keyboard=True, input_field_placeholder="Выберите элемент меню")

	return keyboard
