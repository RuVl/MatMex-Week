from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from config import SUPPORT_CHAT_ID
from filters import LocalizedTextFilter
from keyboards.common import menu_kb, cancel_kb
from keyboards.callback_factories import SupportFactory
from state_machines.help import HelpActions

support_router = Router()


@support_router.message(LocalizedTextFilter("btn-support"))
async def handle_support_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("helping"), reply_markup=cancel_kb(l10n))
	await state.set_state(HelpActions.MESSAGE_OR_CANCEL)


@support_router.message(HelpActions.MESSAGE_OR_CANCEL, LocalizedTextFilter("btn-cancel"))
async def handle_support_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	menu = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("cancel_message"), reply_markup=menu)
	await state.clear()


@support_router.message(HelpActions.MESSAGE_OR_CANCEL)
async def handle_support_message(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.bot.send_message(chat_id=SUPPORT_CHAT_ID,
							   text=l10n.format_value("new-support-question"))
	await msg.bot.send_message(chat_id=SUPPORT_CHAT_ID,
							   text=msg.text + "\n||" + SupportFactory(user_id=msg.from_user.id, message_id=msg.message_id).pack() + "||")
	menu = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("send-helping"), reply_markup=menu)
	await state.clear()
