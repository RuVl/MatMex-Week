from aiogram.utils.keyboard import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


def get_category_keyboard() -> ReplyKeyboardMarkup:
	# todo возможно, стоит обращаться к бд и создавать клавиатуру по доступной мерчаге
	buttons_data = [
		"Футболки",
		"Браслеты",
		"Обложки на студ.билеты",
		"Шопперы",
		"Отмена"
	]
	buttons = [
		KeyboardButton(text=text)
		for text in buttons_data
	]
	keyboard = ReplyKeyboardMarkup(keyboard=[
		buttons[:2],
		buttons[2:4],
		buttons[4:]
	], resize_keyboard=True, input_field_placeholder="Выберите категорию")
	return keyboard
