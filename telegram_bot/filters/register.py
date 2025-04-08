import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

from database import async_session
from database.methods import get_user_by_telegram_id

class FIO_filter(BaseFilter):
	async def __call__(self, message: Message) -> bool:
		fio_pattern = re.compile(r'^[А-ЯЁа-яё]+(?:[-][А-ЯЁа-яё]+)*\s+[А-ЯЁа-яё]+(?:[-][А-ЯЁа-яё]+)*\s*(?:[А-ЯЁа-яё]+(?:[-][А-ЯЁа-яё]+)*)?$')
		return fio_pattern.match(message.text.strip())

class is_not_registered_filter():
	async def __call__(self, message: Message) -> bool:
		async with async_session() as session:
			return await get_user_by_telegram_id(session, message.from_user.id) == None
