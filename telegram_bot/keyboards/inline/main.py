from aiogram.filters.callback_data import CallbackData

class SupportFactory(CallbackData, prefix='support'):
	user_id: int
	message_id: int