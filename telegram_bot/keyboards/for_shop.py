from aiogram.utils.keyboard import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup


def get_category_keyboard() -> ReplyKeyboardMarkup:
	# todo возможно, стоит обращаться к бд и создавать клавиатуру по доступной мерчаге
	buttons_data = [
		("Футболки", "shirts"),
		("Браслеты", "braslets"),
		("Обложки на студ.билеты", "cards"),
		("Шопперы", "shoppers"),
		("Отмена", "cancel")
	]
	buttons = [
		KeyboardButton(text=text, callback_data=callback_data)
		for text, callback_data in buttons_data
	]
	keyboard = ReplyKeyboardMarkup(keyboard=[
		buttons[:2],
		buttons[2:4],
		buttons[4:]
	], resize_keyboard=True, input_field_placeholder="Выберите категорию")
	return keyboard
