import re
from functools import cached_property

from aiogram.filters import BaseFilter
from aiogram.types import Message


class FullNameFilter(BaseFilter):
	async def __call__(self, msg: Message) -> bool:
		if msg.text is None:
			return False

		return self.pattern.match(msg.text.strip())

	@cached_property
	def pattern(self) -> re.Pattern:
		return re.compile(
			r'^[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*'  # Фамилия
			r'\s+[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*'  # Имя
			# Отчество (опционально)
			r'(?:\s+[А-ЯЁа-яё]+(?:-[А-ЯЁа-яё]+)*)?$'
		)
