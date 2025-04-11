from aiogram.filters.callback_data import CallbackData

class SupportCallback(CallbackData, prefix=''):
	command: str
	user_id: int
	message_id: int