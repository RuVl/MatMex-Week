from aiogram import types


def get_cancel_keyboard():
	keyboard = types.ReplyKeyboardMarkup(keyboard=[
		[types.KeyboardButton(text="Отмена", callback_data="cancel")]
	], resize_keyboard=True)
	return keyboard
