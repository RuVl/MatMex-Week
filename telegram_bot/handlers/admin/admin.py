from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from filters import LocalizedTextFilter
from keyboards.common import get_admin_kb, get_menu_kb
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
