from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_account_menu_keyboard():
	buttons_data = [
		("Редактировать ФИО", "edit_FIO"),
		("Я вообще-то в пк", "pk_apply"),
  		("В меню", "back_to_menu"),
	]

	buttons = [
		KeyboardButton(text=text, callback_data=callback_data)
		for text, callback_data in buttons_data
	]

	keyboard = ReplyKeyboardMarkup(keyboard=[
		buttons[:2],
		buttons[2:]
	], resize_keyboard=True, input_field_placeholder="Выберите элемент меню")

	return keyboard