from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_keyboard():
	buttons_data = [
		("Магазин", "shop"),
		("Профиль", "profile"),
		("Поддержка", "help"),
		("Расписание", "schedule"),
		("Мой код", "my_code"),
		("Ввести Промокод", "promo_code")
	]

	buttons = [
		KeyboardButton(text=text, callback_data=callback_data)
		for text, callback_data in buttons_data
	]

	keyboard = ReplyKeyboardMarkup(keyboard=[
		buttons[:3],
		buttons[3:],
	], resize_keyboard=True, input_field_placeholder="Выберите элемент меню")

	return keyboard
