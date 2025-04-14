import os
from aiogram import F
from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from keyboards.common import get_edit_shop_kb, get_cancel_kb, get_admin_kb, get_category_kb, get_item_kb, get_item_size_kb, get_yes_no_cancel_kb
from state_machines.states_admin import AdminActions
from state_machines.states_edit_shop import EditShopActions
from filters.main import LocalizedTextFilter
from config import MEDIA_DIR
from database.methods import create_category, get_category, remove_category, create_item, remove_item, get_item
from database import async_session
from database.enums import MerchSize
edit_shop_router = Router()

@edit_shop_router.message(AdminActions.ADMIN_PANEL,
                          LocalizedTextFilter("btn-edit-shop"))
async def handle_edit_shop(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_edit_shop")
	await msg.answer(l10n.format_value("edit-shop-menu"), reply_markup=get_edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state="cleared")

@edit_shop_router.message(EditShopActions.EDIT_SHOP,
                          LocalizedTextFilter("btn-back"))
async def handle_back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_back_to_menu")
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=get_admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)
	await log.adebug("log-state-changed", state="AdminActions.ADMIN_PANEL")

@edit_shop_router.message(
	or_f(EditShopActions.CREATE_CATEGORY, 
      EditShopActions.EDIT_CATEGORY, 
      EditShopActions.DELETE_CATEGORY, 
      EditShopActions.CREATE_ITEM,
      EditShopActions.CHOOSE_ITEM_NAME,
      EditShopActions.CHOOSE_ITEM_SIZE,
      EditShopActions.CHOOSE_ITEM_FULL_PRICE,
      EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE,
	  EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT,
	  EditShopActions.CHOOSE_ITEM_IN_STOCK,
   	  EditShopActions.CHOOSE_ITEM_IMAGE,
      EditShopActions.DELETE_ITEM_CHOOSE_CATEGORY,
      EditShopActions.DELETE_ITEM,
      ),
	or_f(LocalizedTextFilter("btn-cancel"), LocalizedTextFilter("btn-back"))
)
async def handle_cancel_edit(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_cancel_edit")
	await msg.answer(l10n.format_value("cancel_edit_shop"), reply_markup=get_edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state="EditShopActions.EDIT_SHOP")

@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-back"))
async def handle_back(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_category")
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=get_admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)
	await log.adebug("log-state-changed", state="AdminActions.ADMIN_PANEL")

@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-add-category"))
async def handle_create_category_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_category_btn")
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.CREATE_CATEGORY)
	await log.adebug("log-state-changed", state="EditShopActions.CREATE_CATEGORY")

@edit_shop_router.message(EditShopActions.CREATE_CATEGORY)
async def handle_create_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_category")
	if not msg.photo:
		await msg.answer(l10n.format_value("no-photo"), reply_markup=get_cancel_kb(l10n))
		return
	if not msg.caption:
		await msg.answer(l10n.format_value("no-text"), reply_markup=get_cancel_kb(l10n))
		return
	name = msg.caption.strip()
	save_folder = MEDIA_DIR / "categories" 
	os.makedirs(save_folder, exist_ok=True)
	save_location = save_folder / (name + ".jpg")
	file = await msg.bot.get_file(msg.photo[-1].file_id)
	res = await msg.bot.download_file(file_path=file.file_path, destination=save_location)
	"""if not res:
		await msg.answer(l10n.format_value("failed-download"), reply_markup=get_cancel_kb(l10n))
		return"""

	async with async_session() as session:
		category = await create_category(session=session, name=name, image_path=str(save_location))
	if category is None:
		await msg.answer(l10n.format_value("category-name-already-exists"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("category-created"), reply_markup=get_edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state="EditShopActions.EDIT_SHOP")

@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-delete-category"))
async def handle_delete_category_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_category_btn")
	category_kb = await get_category_kb(l10n)
	await msg.answer(l10n.format_value("ask-for-category"), reply_markup=category_kb)
	await state.set_state(EditShopActions.DELETE_CATEGORY)
	await log.adebug("log-state-changed", state="EditShopActions.DELETE_CATEGORY")


@edit_shop_router.message(EditShopActions.DELETE_CATEGORY)
async def handle_delete_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_category")
	async with async_session() as session:
		category = await get_category(session, msg.text)
		result = await remove_category(session=session, category=category)
	if result:
		await msg.answer(l10n.format_value("category-deleted"), reply_markup=get_edit_shop_kb(l10n))
		await state.set_state(EditShopActions.EDIT_SHOP)
		await log.adebug("log-state-changed", state="EditShopActions.EDIT_SHOP")
	else:
		await msg.answer(l10n.format_value("category-not-deleted"), reply_markup=get_cancel_kb(l10n))
'''
@edit_shop_router.message(EditShopActions.EDIT_SHOP, F.text == "Редактировать категорию")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.EDIT_CATEGORY)


@edit_shop_router.message(EditShopActions.EDIT_CATEGORY)
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-category"), reply_markup=get_edit_item_kb(l10n))
	await state.set_state(EditShopActions.IN_CATEGORY)

'''

@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-add-item"))
async def handle_create_item_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_item_btn")
	category_kb = await get_category_kb(l10n)
	await msg.answer(l10n.format_value("ask-for-category"), reply_markup=category_kb)
	await state.set_state(EditShopActions.CREATE_ITEM)
	await log.adebug("log-state-changed", state="EditShopActions.CREATE_ITEM")


@edit_shop_router.message(EditShopActions.CREATE_ITEM)
async def handle_create_item(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_item")
	async with async_session() as session:
		category = await get_category(session=session, name=msg.text)
	if category:
		await msg.answer(l10n.format_value("ask-for-item-name"), reply_markup=get_cancel_kb(l10n))
		await state.update_data(category_id = category.id)
		await state.set_state(EditShopActions.CHOOSE_ITEM_NAME)
		await log.adebug("log-state-changed", state="EditShopActions.CHOOSE_ITEM_NAME")
	else:
		await msg.answer(l10n.format_value("category-not-exists"), reply_markup=get_cancel_kb(l10n))

@edit_shop_router.message(EditShopActions.CHOOSE_ITEM_NAME)
async def handle_ask_for_item_name(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_name")
	await msg.answer(l10n.format_value("ask-for-item-size"), reply_markup=get_item_size_kb(l10n))
	await state.update_data(item_name = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_SIZE)
	await log.adebug("log-state-changed", state="EditShopActions.CHOOSE_ITEM_SIZE")

@edit_shop_router.message(EditShopActions.CHOOSE_ITEM_SIZE)
async def handle_ask_for_item_size(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_size")
	if not msg.text in [size.value for size in MerchSize]:
		await msg.answer(l10n.format_value("wrong-size"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-full-price"), reply_markup=get_cancel_kb(l10n))
	await state.update_data(item_size = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_FULL_PRICE)
	await log.adebug("log-state-changed", state="EditShopActions.CHOOSE_ITEM_FULL_PRICE")
 
@edit_shop_router.message(EditShopActions.CHOOSE_ITEM_FULL_PRICE)
async def handle_ask_for_item_full_prcie(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_full_prcie")
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-discount-price"), reply_markup=get_cancel_kb(l10n))
	await state.update_data(item_full_price = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)
	await log.adebug("log-state-changed", state="EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE")

@edit_shop_router.message(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)
async def handle_ask_for_item_discount_pice(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_discount_pice")
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-available-count"), reply_markup=get_cancel_kb(l10n))
	await state.update_data(item_discount_price = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)
	await log.adebug("log-state-changed", state="EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT")

@edit_shop_router.message(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)
async def handle_ask_for_item_available_count(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_discount_pice")
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-in-stock"), reply_markup=get_yes_no_cancel_kb(l10n))
	await state.update_data(item_available_count = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_IN_STOCK)
	await log.adebug("log-state-changed", state="EditShopActions.CHOOSE_ITEM_IN_STOCK")

@edit_shop_router.message(EditShopActions.CHOOSE_ITEM_IN_STOCK)
async def handle_ask_for_item_in_stock(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_in_stock")
	if not msg.text in [l10n.format_value("btn-yes"), l10n.format_value("btn-no")]:
		await msg.answer(l10n.format_value("not-a-yes-no"), reply_markup=get_yes_no_cancel_kb(l10n))
		return
	if msg.text == l10n.format_value("btn-yes"):
		await state.update_data(item_in_stock = True)
	else:
		await state.update_data(item_in_stock = False)
	await msg.answer(l10n.format_value("ask-for-item-image"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.CHOOSE_ITEM_IMAGE)
	await log.adebug("log-state-changed", state="EditShopActions.CHOOSE_ITEM_IMAGE")

@edit_shop_router.message(EditShopActions.CHOOSE_ITEM_IMAGE)
async def handle_ask_for_item_image(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_image")
	data = await state.get_data()
	if not msg.photo:
		await msg.answer(l10n.format_value("no-photo"), reply_markup=get_cancel_kb(l10n))
		return
	save_folder = MEDIA_DIR / "merch_items" 
	os.makedirs(save_folder, exist_ok=True)
	save_location = save_folder / (data.get("item_name") + ".jpg")
	file = await msg.bot.get_file(msg.photo[-1].file_id)
	res = await msg.bot.download_file(file_path=file.file_path, destination=save_location)
	"""if not res:
		await msg.answer(l10n.format_value("failed-download"), reply_markup=get_cancel_kb(l10n))
		return"""
	async with async_session() as session:
		item = await create_item(session=session, 
                           name=data.get("item_name"), 
                           image_path=str(save_location),
                           size=data.get("item_size"),
                           full_price = float(data.get("item_full_price")),
                           discount_price = float(data.get("item_discount_price")),
                           available_count = int(data.get("item_available_count")),
                           in_stock = bool(data.get("item_in_stock")),
                           category_id=int(data.get("category_id")))
	if not item:
		await msg.answer(l10n.format_value("item-create-error"), reply_markup=get_edit_shop_kb(l10n))
	else:
		await msg.answer(l10n.format_value("item-created"), reply_markup=get_edit_shop_kb(l10n))
	await state.clear()
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state="EditShopActions.EDIT_SHOP")

@edit_shop_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-delete-item"))
async def handle_delete_item_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_item_btn")
	category_kb = await get_category_kb(l10n)
	await msg.answer(l10n.format_value("ask-for-category"), reply_markup=category_kb)
	await state.set_state(EditShopActions.DELETE_ITEM_CHOOSE_CATEGORY)
	await log.adebug("log-state-changed", state="EditShopActions.DELETE_ITEM_CHOOSE_CATEGORY")

@edit_shop_router.message(EditShopActions.DELETE_ITEM_CHOOSE_CATEGORY)
async def handle_delete_item_choose_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_item_choose_category")
	async with async_session() as session:
		category = await get_category(session, msg.text)
	if not category:
		category_kb = await get_category_kb(l10n)
		await msg.answer(l10n.format_value("category-not-exists"), reply_markup=category_kb)
		return
	await msg.answer(l10n.format_value("ask-for-item-name"), reply_markup=get_item_kb(l10n, category))
	await state.update_data(category_name = category.name)
	await state.set_state(EditShopActions.DELETE_ITEM)
	await log.adebug("log-state-changed", state="EditShopActions.DELETE_ITEM")

@edit_shop_router.message(EditShopActions.DELETE_ITEM)
async def handle_delete_item(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_item_btn")
	async with async_session() as session:
		item = await get_item(session, msg.text)
		result = await remove_item(session, item)
	if not result:
		data = await state.get_data()
		category = await get_category(session, data.get("category_name"))
		category_kb = await get_item_kb(l10n, category)
		await msg.answer(l10n.format_value("item-not-exists"), reply_markup=get_item_kb(l10n, category_kb))
		return
	await msg.answer(l10n.format_value("item-deleted"), reply_markup=get_edit_shop_kb(l10n))
	await state.clear()
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state="EditShopActions.EDIT_SHOP")