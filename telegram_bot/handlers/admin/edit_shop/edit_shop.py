from aiogram import F
from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from keyboards.common import get_edit_shop_kb, get_cancel_kb, get_admin_kb, get_edit_item_kb
from state_machines.states_admin import AdminActions
from state_machines.states_edit_shop import EditShopActions

edit_shop_router = Router()
edit_shop_router.message.filter(
	F.text  # todo добавить чек на права из базы данных
)


@edit_shop_router.message(AdminActions.ADMIN_PANEL, F.text == "Редактировать магазин")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-shop-menu"), reply_markup=get_edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(EditShopActions.EDIT_SHOP, F.text == "Добавить категорию")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.CREATE_CATEGORY)


@edit_shop_router.message(
	or_f(EditShopActions.CREATE_CATEGORY, EditShopActions.EDIT_CATEGORY, EditShopActions.EDIT_SHOP),
	F.text == "Отмена"
)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("creating-category-cancelled"), reply_markup=get_admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@edit_shop_router.message(EditShopActions.CREATE_CATEGORY)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("create-category"), reply_markup=get_edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(EditShopActions.EDIT_SHOP, F.text == "Редактировать категорию")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.EDIT_CATEGORY)


@edit_shop_router.message(EditShopActions.EDIT_CATEGORY)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-category"), reply_markup=get_edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)


@edit_shop_router.message(EditShopActions.IN_CATEGORY, F.text == "Удалить товар")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-name-item"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.DELETE_ITEM)


@edit_shop_router.message(EditShopActions.IN_CATEGORY, F.text == "Добавить товар")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-name-item"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.CREATE_ITEM)


@edit_shop_router.message(
	or_f(EditShopActions.CREATE_ITEM, EditShopActions.DELETE_ITEM, EditShopActions.SET_SIZE, EditShopActions.SET_PRICE, EditShopActions.SET_COUNT),
	F.text == "Отмена"
)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("cancel-edit-item"), reply_markup=get_edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)


@edit_shop_router.message(EditShopActions.DELETE_ITEM)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("delete-item"), reply_markup=get_edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)


@edit_shop_router.message(EditShopActions.CREATE_ITEM)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-size"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.SET_SIZE)


@edit_shop_router.message(EditShopActions.SET_SIZE)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-price"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.SET_PRICE)


@edit_shop_router.message(EditShopActions.SET_PRICE)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-count"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.SET_COUNT)


@edit_shop_router.message(EditShopActions.SET_COUNT)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("create-item"), reply_markup=get_edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)
