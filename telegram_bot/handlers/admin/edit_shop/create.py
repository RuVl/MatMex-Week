
import os
from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from keyboards.common import get_edit_shop_kb, get_cancel_kb, get_category_kb, get_item_size_kb, get_yes_no_cancel_kb
from keyboards.inline import get_category_ikb
from state_machines.states_edit_shop import EditShopActions
from filters.main import LocalizedTextFilter
from config import MEDIA_DIR
from database.methods import create_category, get_category_by_name, create_item
from database import async_session
from database.enums import MerchSize

edit_shop_create_router = Router()

@edit_shop_create_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-add-category"))
async def handle_create_category_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_category_btn")
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(EditShopActions.CREATE_CATEGORY)
	await log.adebug("log-state-changed", state=EditShopActions.CREATE_CATEGORY.state)

@edit_shop_create_router.message(EditShopActions.CREATE_CATEGORY)
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
	file = await msg.bot.get_file(msg.photo[-1].file_id)
	save_location = save_folder / (name + '.jpg')
	await msg.bot.download_file(file_path=file.file_path, destination=save_location)

	async with async_session() as session:
		category = await create_category(session=session, name=name, image_path=str(save_location))
	if category is None:
		await msg.answer(l10n.format_value("category-name-already-exists"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("category-created"), reply_markup=get_edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state=EditShopActions.EDIT_SHOP.state)

@edit_shop_create_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-add-item"))
async def handle_create_item_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_item_btn")
	category_kb = await get_category_kb(l10n)
	await msg.answer(l10n.format_value("ask-for-category"), reply_markup=category_kb)
	await state.set_state(EditShopActions.CREATE_ITEM)
	await log.adebug("log-state-changed", state=EditShopActions.CREATE_ITEM.state)


@edit_shop_create_router.message(EditShopActions.CREATE_ITEM)
async def handle_create_item(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_item")
	async with async_session() as session:
		category = await get_category_by_name(session=session, name=msg.text)
	if category:
		await msg.answer(l10n.format_value("ask-for-item-name"), reply_markup=get_cancel_kb(l10n))
		await state.update_data(category_id = category.id)
		await state.set_state(EditShopActions.CHOOSE_ITEM_NAME)
		await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_NAME.state)
	else:
		await msg.answer(l10n.format_value("category-not-exists"), reply_markup=get_cancel_kb(l10n))

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_NAME, F.text)
async def handle_ask_for_item_name(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_name")
	await msg.answer(l10n.format_value("ask-for-item-size"), reply_markup=get_item_size_kb(l10n))
	await state.update_data(item_name = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_SIZE)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_SIZE.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_SIZE)
async def handle_ask_for_item_size(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_size")
	if not msg.text in [size.value for size in MerchSize]:
		await msg.answer(l10n.format_value("wrong-size"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-full-price"), reply_markup=get_cancel_kb(l10n))
	await state.update_data(item_size = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_FULL_PRICE)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_FULL_PRICE.state)
 
@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_FULL_PRICE)
async def handle_ask_for_item_full_prcie(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_full_prcie")
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-discount-price"), reply_markup=get_cancel_kb(l10n))
	await state.update_data(item_full_price = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)
async def handle_ask_for_item_discount_pice(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_discount_pice")
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-available-count"), reply_markup=get_cancel_kb(l10n))
	await state.update_data(item_discount_price = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)
async def handle_ask_for_item_available_count(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_discount_pice")
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"), reply_markup=get_cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("ask-for-item-in-stock"), reply_markup=get_yes_no_cancel_kb(l10n))
	await state.update_data(item_available_count = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_IN_STOCK)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_IN_STOCK.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_IN_STOCK)
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
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_IMAGE.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_IMAGE)
async def handle_ask_for_item_image(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_image")
	data = await state.get_data()
	if not msg.photo:
		await msg.answer(l10n.format_value("no-photo"), reply_markup=get_cancel_kb(l10n))
		return
	save_folder = MEDIA_DIR / "merch_items" 
	os.makedirs(save_folder, exist_ok=True)
	file = await msg.bot.get_file(msg.photo[-1].file_id)
	save_location = save_folder / (data.get("item_name") + '.jpg')
	await msg.bot.download_file(file_path=file.file_path, destination=save_location)
	async with async_session() as session:
		await create_item(
						session=session, 
						name=data.get("item_name"), 
						image_path=str(save_location),
						size=data.get("item_size"),
						full_price = float(data.get("item_full_price")),
						discount_price = float(data.get("item_discount_price")),
						available_count = int(data.get("item_available_count")),
						in_stock = bool(data.get("item_in_stock")),
						category_id=int(data.get("category_id")))
	await msg.answer(l10n.format_value("item-created"), reply_markup=get_edit_shop_kb(l10n))
	await state.clear()
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state=EditShopActions.EDIT_SHOP.state)

@edit_shop_create_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-delete-item-or-category"))
async def handle_delete_category_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_delete_category_btn")	
	text = l10n.format_value("shop-hello")
	image_from_pc = types.FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	category_ikb = await get_category_ikb(l10n, True)
	await msg.answer_photo(
		image_from_pc,
		caption=text,
		reply_markup=category_ikb
	)
	await log.adebug("log-state-changed", state=EditShopActions.EDIT_SHOP.state)
