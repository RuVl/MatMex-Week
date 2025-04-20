from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database.enums import AdminPrivilege
from filters import LocalizedTextFilter, PrivilegeFilter
from keyboards.common import admin_kb, menu_kb
from state_machines.admin import AdminActions
from .code_scanner import code_scanner_router
from .edit_shop import edit_shop_main_router
from .grant_privileges import grant_privileges_router

admin_menu_router = Router()
admin_menu_router.include_routers(
	code_scanner_router,
	edit_shop_main_router,
	grant_privileges_router
)

admin_menu_router.message.filter(PrivilegeFilter(AdminPrivilege.ALL))
admin_menu_router.callback_query.filter(PrivilegeFilter(AdminPrivilege.ALL))


@admin_menu_router.message(LocalizedTextFilter("btn-admin-panel"))
async def handle_admin_panel(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="open_admin_panel")
	await msg.answer(l10n.format_value("hello-admin"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@admin_menu_router.message(AdminActions.ADMIN_PANEL, LocalizedTextFilter("btn-back-to-menu"))
async def handle_back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="back_to_menu")
	menu = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=menu)
	await state.clear()
