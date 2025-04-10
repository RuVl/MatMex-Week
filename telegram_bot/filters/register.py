import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

from database import async_session
from database.methods import user_exist_with_telegram_id


class IsNotRegisteredFilter(BaseFilter):
	async def __call__(self, msg: Message) -> bool:
		async with async_session() as session:
			return not await user_exist_with_telegram_id(session, msg.from_user.id)


class FullNameFilter(BaseFilter):
	async def __call__(self, msg: Message) -> bool:
		name_pattern = re.compile(
			r'^[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*'  # Фамилия
			r'\s+[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*'  # Имя
			r'(?:\s+[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*)?$'  # Отчество (опционально)
		)
		return name_pattern.match(msg.text.strip())
