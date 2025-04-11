from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from utils import SupportCallback
from filters import LocalizedTextFilter
from keyboards.common import get_admin_kb, get_menu_kb, get_cancel_inline_kb, get_send_support_inline_kb
from state_machines.states_admin import AdminActions
from .code_scanner import code_scanner_router
from .edit_shop import edit_shop_router

admin_router = Router()
admin_router.message.filter(
	F.text  # TODO добавить чек на права из базы данных
)
admin_router.include_routers(code_scanner_router, edit_shop_router)


@admin_router.message(LocalizedTextFilter("btn-admin-panel"))
async def handle_admin_panel(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="open_admin_panel")
	await msg.answer(l10n.format_value("hello-admin"), reply_markup=get_admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)
	await log.adebug("log-state-changed", state=AdminActions.ADMIN_PANEL.state)


@admin_router.message(AdminActions.ADMIN_PANEL, LocalizedTextFilter("btn-back-to-menu"))
async def handle_back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="back_to_menu")
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=get_menu_kb(l10n))
	await state.clear()
	await log.adebug("log-state-changed", state="cleared")


@admin_router.callback_query(F.data.startswith(":send_support"))
async def handle_send_support_button(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization):
	await callback.answer(l10n.format_value("wait-send-support"))
	data = SupportCallback.unpack(callback.data)
	user_id = data.user_id
	message_id = data.message_id
	await callback.message.edit_reply_markup(reply_markup=get_cancel_inline_kb(l10n, data))
	await state.update_data(user_id=user_id, message_id=message_id)
	await state.set_state(AdminActions.SEND_SUPPORT)

@admin_router.callback_query(AdminActions.SEND_SUPPORT, F.data.startswith(":cancel_send_support"))
async def handle_cancel_send_support_button(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization):
	data = SupportCallback.unpack(callback.data)
	await callback.answer(l10n.format_value("cancel-send-support"))
	await callback.message.edit_reply_markup(reply_markup=get_send_support_inline_kb(l10n, data))
	await state.clear()

@admin_router.message(AdminActions.SEND_SUPPORT)
async def handle_send_support(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="back_to_menu")
	data = await state.get_data()
	user_id = data.get('user_id')
	message_id = data.get('message_id')
	await msg.bot.send_message(chat_id = user_id, text = l10n.format_value("support-answer"), reply_to_message_id=message_id)
	await msg.bot.send_message(chat_id = user_id, text = msg.text)
	await msg.answer(l10n.format_value("support-sent"))
	await state.clear()
	await log.adebug("log-state-changed", state="cleared")
