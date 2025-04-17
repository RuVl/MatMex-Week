import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class FullNameFilter(BaseFilter):
	async def __call__(self, msg: Message) -> bool:
		if msg.text is None:
			return False

		name_pattern = re.compile(
			r'^[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*'  # Фамилия
			r'\s+[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*'  # Имя
			r'(?:\s+[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*)?$'  # Отчество (опционально)
		)
		return name_pattern.match(msg.text.strip())
