from typing import Literal

from aiogram.filters.callback_data import CallbackData


class PKApplyFactory(CallbackData, prefix='apply'):
	apply_id: int
	decision: Literal['approve', 'reject', 'review']


class SupportFactory(CallbackData, prefix='support'):
	user_id: int
	message_id: int

class PrivilegeButtonFactory(CallbackData, prefix='privilege_button'):
    privilege: int
    granted: bool
    admin_id: int
    subject_id: int

class UserFactory(CallbackData, prefix='user_data'):
    full_name: str
    telegram_id: int
    telegram_username: str
    