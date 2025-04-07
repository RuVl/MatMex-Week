from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from aiogram import F
from aiogram.filters import or_f

from keyboards import get_edit_shop_keyboard, get_cancel_keyboard, get_admin_keyboard
from state_machines.states_admin import AdminActions
from state_machines.states_edit_shop import EditShopActions

edit_shop_router = Router()
edit_shop_router.message.filter(
    F.text #todo добавить чек на права из датабазы
)

@edit_shop_router.message(AdminActions.ADMIN_PANEL,
                            F.text == "Редактировать магазин")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-shop-menu"), reply_markup=get_edit_shop_keyboard())
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(EditShopActions.EDIT_SHOP,
                            F.text == "Добавить категорию")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=get_cancel_keyboard())
	await state.set_state(EditShopActions.CREATE_CATEGORY)


@edit_shop_router.message(or_f(EditShopActions.CREATE_CATEGORY, EditShopActions.EDIT_CATEGORY, EditShopActions.EDIT_SHOP),
                            F.text == "Отмена")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("creating-category-cancelled"), reply_markup=get_admin_keyboard())
	await state.set_state(AdminActions.ADMIN_PANEL)


@edit_shop_router.message(EditShopActions.CREATE_CATEGORY)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("create-category"), reply_markup=get_edit_shop_keyboard())
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(EditShopActions.EDIT_SHOP,
                            F.text == "Редактировать категорию")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=get_cancel_keyboard())
	await state.set_state(EditShopActions.EDIT_CATEGORY)


@edit_shop_router.message(EditShopActions.EDIT_CATEGORY)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-category"), reply_markup=get_edit_shop_keyboard())
	await state.set_state(EditShopActions.EDIT_SHOP)
