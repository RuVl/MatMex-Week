from aiogram import F, Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database.enums import AdminPrivilege
from filters.main import LocalizedTextFilter, PrivilegeFilter
from keyboards.common import admin_kb, edit_shop_kb
from state_machines.admin import AdminActions
from state_machines.edit_shop import EditShopActions
from .create import create_router
from .delete import delete_router

edit_shop_router = Router()
edit_shop_router.include_routers(
	create_router,
	delete_router
)

edit_shop_router.message.filter(PrivilegeFilter(AdminPrivilege.EDIT_SHOP))
edit_shop_router.callback_query.filter(PrivilegeFilter(AdminPrivilege.EDIT_SHOP))


@edit_shop_router.message(AdminActions.ADMIN_PANEL, LocalizedTextFilter("btn-edit-shop"))
async def edit_shop_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-shop-menu"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(
	EditShopActions.CREATE_CATEGORY,
	LocalizedTextFilter("btn-cancel"),
)
async def cancel_edit_category_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("cancel-edit-shop"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


# TODO ПЕРЕДЕЛАТЬ ЭТУ ПАРАШУ
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
async def cancel_edit_item_h(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization):
	await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
	await callback.message.answer(l10n.format_value("cancel-edit-shop"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-back"))
async def back_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)
