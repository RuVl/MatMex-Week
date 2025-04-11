from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from filters import LocalizedTextFilter
from keyboards.common import get_menu_kb, get_cancel_kb
from state_machines.states_help import HelpActions
from config import SUPPORT_CHAT_ID
from keyboards.inline import SupportFactory
support_router = Router()


@support_router.message(LocalizedTextFilter("btn-support"))
async def handle_support_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await msg.answer(l10n.format_value("helping"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(HelpActions.MESSAGE_OR_CANCEL)
	await log.adebug("log-state-changed", state=HelpActions.MESSAGE_OR_CANCEL.state)


@support_router.message(HelpActions.MESSAGE_OR_CANCEL, LocalizedTextFilter("btn-cancel"))
async def handle_support_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await msg.answer(l10n.format_value("cancel_message"), reply_markup=get_menu_kb(l10n))
	await state.clear()
	await log.adebug("log-state-changed", state="cleared")


@support_router.message(HelpActions.MESSAGE_OR_CANCEL)
async def handle_support_message(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	# user_question = msg.text
	# user_id = msg.from_user.id
	# TODO отправить в чат админов
	await msg.bot.send_message(chat_id=SUPPORT_CHAT_ID, 
                            text=l10n.format_value("new-support-question"))
	await msg.bot.send_message(chat_id=SUPPORT_CHAT_ID,
                            text = SupportFactory(user_id = msg.from_user.id, message_id=msg.message_id).pack() + "\n"+ msg.text)
	await msg.answer(l10n.format_value("send-helping"), reply_markup=get_menu_kb(l10n))
	await state.clear()
	log.info("log-state-changed", state="cleared")
