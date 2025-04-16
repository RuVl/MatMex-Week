from aiogram import F
from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from config import MEDIA_DIR
from database import async_session
from database.methods import create_category
from filters.main import LocalizedTextFilter
from keyboards.common import cancel_kb, edit_item_kb, edit_shop_kb, admin_kb
from state_machines.admin import AdminActions
from state_machines.edit_shop import EditShopActions

edit_shop_router = Router()


@edit_shop_router.message(AdminActions.ADMIN_PANEL,
                          LocalizedTextFilter("btn-edit-shop"))
async def handle_edit_shop(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_edit_shop")
	await msg.answer(l10n.format_value("edit-shop-menu"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(
	or_f(EditShopActions.CREATE_CATEGORY, EditShopActions.EDIT_CATEGORY, EditShopActions.EDIT_SHOP),
	LocalizedTextFilter("btn-cancel")
)
async def handle_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_cancel")
	await msg.answer(l10n.format_value("creating-category-cancelled"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-back"))
async def handle_back(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_category")
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-add-category"))
async def handle_create_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_category")
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.CREATE_CATEGORY)


@edit_shop_router.message(EditShopActions.CREATE_CATEGORY)
async def handle_create_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	# TODO: функция сохранения пикчи
	await log.adebug("log-admin-action", action="handle_create_category")
	if not msg.photo:
		await msg.answer(l10n.format_value("no-photo"), reply_markup=cancel_kb(l10n))
		return
	if not msg.caption:
		await msg.answer(l10n.format_value("no-text"), reply_markup=cancel_kb(l10n))
		return
	name = msg.caption.strip()
	save_folder = MEDIA_DIR / "categories"
	save_folder.mkdir(exist_ok=True)
	save_location = save_folder / (name + ".jpg")
	file = await msg.bot.get_file(msg.photo[-1].file_id)
	res = msg.bot.download_file(file_path=file.file_path, destination=save_location)
	if not res:
		await msg.answer(l10n.format_value("failed-download"), reply_markup=cancel_kb(l10n))
		return

	async with async_session() as session:
		await create_category(session=session, name=name, image_path=str(save_location))
	await msg.answer(l10n.format_value("category-created"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


@edit_shop_router.message(EditShopActions.EDIT_SHOP, F.text == "Редактировать категорию")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.EDIT_CATEGORY)


@edit_shop_router.message(EditShopActions.EDIT_CATEGORY)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-category"), reply_markup=edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)


@edit_shop_router.message(EditShopActions.IN_CATEGORY, F.text == "Удалить товар")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-name-item"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.DELETE_ITEM)


@edit_shop_router.message(EditShopActions.IN_CATEGORY, F.text == "Добавить товар")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-name-item"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.CREATE_ITEM)


@edit_shop_router.message(
	or_f(EditShopActions.CREATE_ITEM, EditShopActions.DELETE_ITEM, EditShopActions.SET_SIZE, EditShopActions.SET_PRICE, EditShopActions.SET_COUNT),
	F.text == "Отмена"
)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("cancel-edit-item"), reply_markup=edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)


@edit_shop_router.message(EditShopActions.DELETE_ITEM)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("delete-item"), reply_markup=edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)


@edit_shop_router.message(EditShopActions.CREATE_ITEM)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-size"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.SET_SIZE)


@edit_shop_router.message(EditShopActions.SET_SIZE)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-price"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.SET_PRICE)


@edit_shop_router.message(EditShopActions.SET_PRICE)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-count"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.SET_COUNT)


@edit_shop_router.message(EditShopActions.SET_COUNT)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("create-item"), reply_markup=edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)
