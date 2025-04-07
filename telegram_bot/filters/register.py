import re
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class FIO_filter(BaseFilter):
	async def __call__(self, message: Message) -> bool:
		fio_pattern = re.compile(r'^([А-Яа-яЁё]+(-[А-Яа-яЁё]+)?\s){2}[А-Яа-яЁё]+(-[А-Яа-яЁё]+)?$')
		return fio_pattern.match(message.text.strip())
