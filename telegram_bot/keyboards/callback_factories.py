from typing import Literal

from aiogram.filters.callback_data import CallbackData


class PKApplyFactory(CallbackData, prefix='apply'):
	apply_id: int
	decision: Literal['approve', 'reject', 'review']


class SupportFactory(CallbackData, prefix='support'):
	user_id: int
	message_id: int
