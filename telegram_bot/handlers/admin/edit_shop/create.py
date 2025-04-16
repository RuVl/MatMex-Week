
import os
from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from keyboards.common import get_edit_shop_kb, get_cancel_kb
from keyboards.inline import EditShopCategoryFactory, get_edit_shop_category_ikb, get_cancel_ikb, get_item_size_ikb, get_yes_no_cancel_ikb
from state_machines.states_edit_shop import EditShopActions
from filters.main import LocalizedTextFilter
from config import MEDIA_DIR
from database.methods import create_category, get_category_by_id, create_item
from database import async_session

edit_shop_create_router = Router()

#TODO: подписывать этап редактирования

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
	category_ikb = await get_edit_shop_category_ikb(l10n)
	await msg.answer(l10n.format_value("item-creation"), reply_markup=types.ReplyKeyboardRemove())
	await msg.answer(l10n.format_value("ask-for-category"), reply_markup=category_ikb)
	await state.set_state(EditShopActions.CREATE_ITEM)
	await log.adebug("log-state-changed", state=EditShopActions.CREATE_ITEM.state)

@edit_shop_create_router.callback_query(EditShopActions.CREATE_ITEM)
async def handle_create_item(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_item")
	callback_data = EditShopCategoryFactory.unpack(callback.data)
	async with async_session() as session:
		category = await get_category_by_id(session, callback_data.category_id)
	if category:
		await callback.bot.edit_message_text(
      										l10n.format_value("ask-for-item-name"), 
                							reply_markup=get_cancel_ikb(l10n),
											chat_id=callback.message.chat.id,
											message_id=callback.message.message_id)
		await state.update_data(category_id = category.id, shop_message_id = callback.message.message_id)
		await state.set_state(EditShopActions.CHOOSE_ITEM_NAME)
		await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_NAME.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_NAME, F.text)
async def handle_ask_for_item_name(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_name")
	state_data = await state.get_data()
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.edit_message_text(
									l10n.format_value("ask-for-item-size"), 
									reply_markup=get_item_size_ikb(l10n),
									chat_id=msg.chat.id,
									message_id=state_data.get("shop_message_id"))
	await state.update_data(item_name = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_SIZE)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_SIZE.state)

@edit_shop_create_router.callback_query(EditShopActions.CHOOSE_ITEM_SIZE)
async def handle_ask_for_item_size(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_size")
	state_data = await state.get_data()
	await callback.message.bot.edit_message_text(
									l10n.format_value("ask-for-item-full-price"), 
									reply_markup=get_cancel_ikb(l10n),
									chat_id=callback.message.chat.id,
									message_id=state_data.get("shop_message_id"))
	await state.update_data(item_size = callback.data)
	await state.set_state(EditShopActions.CHOOSE_ITEM_FULL_PRICE)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_FULL_PRICE.state)
 
@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_FULL_PRICE)
async def handle_ask_for_item_full_price(msg: types.message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_full_prcie")
	state_data = await state.get_data()
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"))
		return
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.edit_message_text(
									l10n.format_value("ask-for-item-discount-price"), 
									reply_markup=get_cancel_ikb(l10n),
									chat_id=msg.chat.id,
									message_id=state_data.get("shop_message_id"))
	await state.update_data(item_full_price = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)
async def handle_ask_for_item_discount_pice(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_discount_pice")
	state_data = await state.get_data()
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"))
		return
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.edit_message_text(
									l10n.format_value("ask-for-item-available-count"), 
									reply_markup=get_cancel_ikb(l10n),
									chat_id=msg.chat.id,
									message_id=state_data.get("shop_message_id"))
	await state.update_data(item_discount_price = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)
async def handle_ask_for_item_available_count(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="ask-for-item-available-count")
	state_data = await state.get_data()
	if not msg.text.isdigit():
		await msg.answer(l10n.format_value("not-a-number"))
		return
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.edit_message_text(
									l10n.format_value("ask-for-item-in-stock"), 
									reply_markup=get_yes_no_cancel_ikb(l10n),
									chat_id=msg.chat.id,
									message_id=state_data.get("shop_message_id"))
	await state.update_data(item_available_count = msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_IN_STOCK)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_IN_STOCK.state)

@edit_shop_create_router.callback_query(EditShopActions.CHOOSE_ITEM_IN_STOCK)
async def handle_ask_for_item_in_stock(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_in_stock")
	state_data = await state.get_data()
	if callback.data == "btn-yes":
		await state.update_data(item_in_stock = True)
	else:
		await state.update_data(item_in_stock = False)
	await callback.bot.edit_message_text(
									l10n.format_value("ask-for-item-image"), 
									reply_markup=get_cancel_ikb(l10n),
									chat_id=callback.message.chat.id,
									message_id=state_data.get("shop_message_id"))
	await state.set_state(EditShopActions.CHOOSE_ITEM_IMAGE)
	await log.adebug("log-state-changed", state=EditShopActions.CHOOSE_ITEM_IMAGE.state)

@edit_shop_create_router.message(EditShopActions.CHOOSE_ITEM_IMAGE)
async def handle_ask_for_item_image(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_item_image")
	state_data = await state.get_data()
	if not msg.photo:
		await msg.answer(l10n.format_value("no-photo"))
		return
	save_folder = MEDIA_DIR / "merch_items" 
	os.makedirs(save_folder, exist_ok=True)
	file = await msg.bot.get_file(msg.photo[-1].file_id)
	save_location = save_folder / (state_data.get("item_name") + '.jpg')
	await msg.bot.download_file(file_path=file.file_path, destination=save_location)
	async with async_session() as session:
		await create_item(
						session=session, 
						name=state_data.get("item_name"), 
						image_path=str(save_location),
						size=state_data.get("item_size"),
						full_price = float(state_data.get("item_full_price")),
						discount_price = float(state_data.get("item_discount_price")),
						available_count = int(state_data.get("item_available_count")),
						in_stock = bool(state_data.get("item_in_stock")),
						category_id=int(state_data.get("category_id")))
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=state_data.get("shop_message_id"))
	await msg.answer(l10n.format_value("item-created"), reply_markup=get_edit_shop_kb(l10n))
	await state.clear()
	await state.set_state(EditShopActions.EDIT_SHOP)
	await log.adebug("log-state-changed", state=EditShopActions.EDIT_SHOP.state)

