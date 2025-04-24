from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.methods import get_privilege_by_user, get_user_by_telegram_id
from env import TelegramKeys


class LocalizedTextFilter(BaseFilter):
	def __init__(self, l10n_key: str):
		self.l10n_key = l10n_key

	async def __call__(self, message: Message, **kwargs) -> bool:
		l10n: FluentLocalization = kwargs.get("l10n")
		if not l10n:
			log: FilteringBoundLogger = kwargs.get("log") or get_logger()
			await log.awarning("l10n context does not set")
			return False

		return message.text == l10n.format_value(self.l10n_key)


class FromBotToAdminFilter(BaseFilter):
	async def __call__(self, message: Message) -> bool:
		return (
				message.reply_to_message and
				message.chat.id == TelegramKeys.ADMIN_CHAT_ID and
				message.reply_to_message.from_user.id == message.bot.id
		)


class AdminPromocodeCreatingFilter(BaseFilter):
	async def __call__(self, msg: Message) -> bool:
		return msg.text.isdecimal() and int(msg.text) > 0


class PrivilegeFilter(BaseFilter):
	def __init__(self, privilege: int):
		self.privilege = privilege

	async def __call__(self, event: Message | CallbackQuery) -> bool:
		async with async_session() as session:
			user = await get_user_by_telegram_id(session, event.from_user.id)
			if user is None:
				return False

			privilege = await get_privilege_by_user(session, user.id)

		return privilege and (privilege.privilege & self.privilege)
