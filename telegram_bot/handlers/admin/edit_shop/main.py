from aiogram import F
from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from keyboards.common import edit_shop_kb, admin_kb
from state_machines.admin import AdminActions
from state_machines.edit_shop import EditShopActions
from filters.main import LocalizedTextFilter, PrivilegeFilter
from database.enums import AdminPrivilege
from .create import create_router
from .delete import delete_router

edit_shop_router = Router()
edit_shop_router.include_routers(
	create_router, delete_router)
edit_shop_router.message.filter(PrivilegeFilter(AdminPrivilege.EDIT_SHOP))
edit_shop_router.callback_query.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_SHOP))


@edit_shop_router.message(AdminActions.ADMIN_PANEL,
							   LocalizedTextFilter("btn-edit-shop"))
async def handle_edit_shop(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_edit_shop")
	await msg.answer(l10n.format_value("edit-shop-menu"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state="cleared")


@edit_shop_router.message(
	EditShopActions.CREATE_CATEGORY,
	LocalizedTextFilter("btn-cancel"),
)
async def handle_cancel_edit_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_cancel_edit_category")
	await msg.answer(l10n.format_value("cancel_edit_shop"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state=EditShopActions.EDIT_SHOP.state)


@edit_shop_router.callback_query(
	or_f(
		EditShopActions.CREATE_ITEM,
		EditShopActions.CHOOSE_ITEM_NAME,
		EditShopActions.CHOOSE_ITEM_SIZE,
		EditShopActions.CHOOSE_ITEM_FULL_PRICE,
		EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE,
		EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT,
		EditShopActions.CHOOSE_ITEM_IN_STOCK,
		EditShopActions.CHOOSE_ITEM_IMAGE,
	),
	F.data == "btn_cancel"
)
async def handle_cancel_edit_item(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_cancel_edit_item")
	await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
	await callback.message.answer(l10n.format_value("cancel_edit_shop"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state=EditShopActions.EDIT_SHOP.state)


@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-back"))
async def handle_back(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_back")
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)
	await log.adebug("log-state-changed", state=AdminActions.ADMIN_PANEL.state)
