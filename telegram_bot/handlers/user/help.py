from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import get_user_by_telegram_id
from env import TelegramKeys
from filters import LocalizedTextFilter
from keyboards.callback_factories import SupportFactory
from keyboards.common import cancel_kb, menu_kb
from state_machines.help import HelpActions

support_router = Router()


@support_router.message(LocalizedTextFilter("btn-support"))
async def support_button_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("helping"), reply_markup=cancel_kb(l10n))
	await state.set_state(HelpActions.MESSAGE_OR_CANCEL)


@support_router.message(HelpActions.MESSAGE_OR_CANCEL, LocalizedTextFilter("btn-cancel"))
async def support_cancel_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	kb = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("cancel-message"), reply_markup=kb)
	await state.clear()


@support_router.message(HelpActions.MESSAGE_OR_CANCEL)
async def support_message_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)

	await msg.bot.send_message(
		chat_id=TelegramKeys.SUPPORT_CHAT_ID,
		text=l10n.format_value("support-question", args={
			"fullname": user.full_name,
			"question": msg.text,
			"metadata": SupportFactory(user_id=msg.from_user.id, message_id=msg.message_id).pack()
		}))

	kb = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("send-helping"), reply_markup=kb)
	await state.clear()
