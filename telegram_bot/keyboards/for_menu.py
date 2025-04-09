from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_keyboard():
	isAdmin = True  # todo чек на права из базы данных
	buttons_data = [
		"Магазин",
		"Профиль",
		"Поддержка",
		"Расписание",
		"Мой код",
		"Ввести Промокод",
		"Админ панель",
	]

	buttons = [
		KeyboardButton(text=text)
		for text in buttons_data
	]

	if isAdmin:
		keyboard = ReplyKeyboardMarkup(keyboard=[
			buttons[:3],
			buttons[3:6],
			buttons[6:]
		], resize_keyboard=True, input_field_placeholder="Выберите элемент меню")
	else:
		keyboard = ReplyKeyboardMarkup(keyboard=[
			buttons[:3],
			buttons[3:6],
		], resize_keyboard=True, input_field_placeholder="Выберите элемент меню")
	return keyboard
