from aiogram.filters import BaseFilter
from aiogram.types import Message
from fluent.runtime import FluentLocalization
from structlog import get_logger
from structlog.typing import FilteringBoundLogger


class LocalizedTextFilter(BaseFilter):
	def __init__(self, l10n_key: str):
		self.l10n_key = l10n_key

	async def __call__(self, message: Message, **kwargs) -> bool:
		l10n: FluentLocalization = kwargs.get("l10n")
		log: FilteringBoundLogger = kwargs.get("log") or get_logger()
		if not l10n:
			await log.awarning("l10n context does not set")
			return False

		return message.text == l10n.format_value(self.l10n_key)
