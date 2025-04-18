from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

from config import SUPPORT_CHAT_ID
from database.methods import get_user_by_telegram_id, get_privilege_by_user
from database import async_session

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
				message.chat.id == SUPPORT_CHAT_ID and
				message.from_user.id == message.bot.id
		)

class AdminPromocodeCreatingFilter(BaseFilter):
	async def __call__(self, msg: Message) -> bool:
		return ( msg.text.isdecimal() and
		          int(msg.text) > 0
		)
class PrivilegeMessageFilter(BaseFilter):
	def __init__(self, privelege : int):
		self.privelege = privelege
	async def __call__(self, message: Message) -> bool:
		async with async_session() as session:
			user = await get_user_by_telegram_id(session, message.from_user.id)
			privilege = await get_privilege_by_user(session, user.id)
		return bool(privilege.privilege & self.privelege)

class PrivilegeCallbackFilter(BaseFilter):
	def __init__(self, privelege : int):
		self.privelege = privelege
	async def __call__(self, callback: CallbackQuery) -> bool:
		async with async_session() as session:
			user = await get_user_by_telegram_id(session, callback.from_user.id)
			privilege = await get_privilege_by_user(session, user.id)
		return bool(privilege.privilege & self.privelege)

