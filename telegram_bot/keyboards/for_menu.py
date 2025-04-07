from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_keyboard():
	isAdmin = True  # todo чек на права из датабазы
	buttons_data = [
		("Магазин", "shop"),
		("Профиль", "profile"),
		("Поддержка", "help"),
		("Расписание", "schedule"),
		("Мой код", "my_code"),
		("Ввести Промокод", "promo_code"),
		("Админ панель", "admin_panel")
	]

	buttons = [
		KeyboardButton(text=text, callback_data=callback_data)
		for text, callback_data in buttons_data
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
