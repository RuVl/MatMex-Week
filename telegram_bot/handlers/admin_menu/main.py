from aiogram import F
from aiogram import Router, types
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from filters import FromBotToAdminFilter
from keyboards.inline import SupportFactory
from .admin_menu import admin_menu_router

admin_main_router = Router()
admin_main_router.message.filter(
	F.text
)
admin_main_router.include_routers(admin_menu_router)

@admin_main_router.message(FromBotToAdminFilter(),
                           F.reply_to_message.text.split("\n")[-1].startswith("support"))
async def handle_send_support(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="send_support")
	original = msg.reply_to_message
	data = SupportFactory.unpack(original.text.split('\n')[-1])
	user_id  = data.user_id
	message_id = data.message_id
	await msg.bot.send_message(chat_id = user_id, text = msg.text, reply_to_message_id=message_id)
	await msg.answer(l10n.format_value("support-sent"))
	await log.adebug("log-state-changed", state="cleared")
