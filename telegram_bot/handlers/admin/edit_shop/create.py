import os

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from database import async_session
from database.methods import create_category, create_item, get_category_by_id
from filters.main import LocalizedTextFilter
from keyboards.callback_factories import EditShopCategoryFactory
from keyboards.common import cancel_kb, edit_shop_kb
from keyboards.inline import cancel_ikb, get_edit_shop_category_ikb, get_item_size_ikb, yes_no_cancel_ikb
from state_machines.edit_shop import EditShopActions

create_router = Router()


# TODO: подписывать этап редактирования


@create_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-add-category"))
async def create_category_btn_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-category-create"), reply_markup=cancel_kb(l10n))
	await state.set_state(EditShopActions.CREATE_CATEGORY)


@create_router.message(EditShopActions.CREATE_CATEGORY)
async def create_category_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	if not msg.photo:
		await msg.answer(l10n.format_value("no-photo"), reply_markup=cancel_kb(l10n))
		return

	if not msg.caption:
		await msg.answer(l10n.format_value("no-text"), reply_markup=cancel_kb(l10n))
		return

	name = msg.caption.strip()
	save_folder = MEDIA_DIR / "categories"
	os.makedirs(save_folder, exist_ok=True)
	file = await msg.bot.get_file(msg.photo[-1].file_id)
	save_location = save_folder / (name + '.jpg')
	await msg.bot.download_file(file_path=file.file_path, destination=save_location)

	async with async_session() as session:
		await create_category(session=session, name=name, image_path=str(save_location))

	await msg.answer(l10n.format_value("category-created"), reply_markup=edit_shop_kb(l10n))
	await state.set_state(EditShopActions.EDIT_SHOP)


@create_router.message(EditShopActions.EDIT_SHOP, LocalizedTextFilter("btn-add-item"))
async def create_item_btn_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	category_ikb = await get_edit_shop_category_ikb(l10n)
	await msg.answer(l10n.format_value("item-creation"), reply_markup=types.ReplyKeyboardRemove())
	await msg.answer(l10n.format_value("ask-for-category"), reply_markup=category_ikb)
	await state.set_state(EditShopActions.CREATE_ITEM)


@create_router.callback_query(EditShopActions.CREATE_ITEM, EditShopCategoryFactory.filter())
async def create_item_h(callback: types.CallbackQuery, callback_data: EditShopCategoryFactory, state: FSMContext, l10n: FluentLocalization):
	async with async_session() as session:
		category = await get_category_by_id(session, callback_data.category_id)

	if category:
		await callback.bot.edit_message_text(
			l10n.format_value("ask-for-item-name"),
			reply_markup=cancel_ikb(l10n),
			chat_id=callback.message.chat.id,
			message_id=callback.message.message_id
		)
		await state.update_data(category_id=category.id, shop_message_id=callback.message.message_id)
		await state.set_state(EditShopActions.CHOOSE_ITEM_NAME)


@create_router.message(EditShopActions.CHOOSE_ITEM_NAME, F.text)
async def ask_for_item_name_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	await msg.delete()
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-item-description"),
		reply_markup=get_item_size_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("shop_message_id")
	)
	await state.update_data(item_name=msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_DESCRIPTION)


@create_router.message(EditShopActions.CHOOSE_ITEM_DESCRIPTION, F.text)
async def ask_for_item_description_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	if msg.text == '-':
		await state.update_data(item_description=None)
		await state.set_state(EditShopActions.CHOOSE_ITEM_SIZE)
		return
	
	state_data = await state.get_data()
	await msg.delete()
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-item-size"),
		reply_markup=get_item_size_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("shop_message_id")
	)
	await state.update_data(item_description=msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_SIZE)


@create_router.callback_query(EditShopActions.CHOOSE_ITEM_SIZE)
async def ask_for_item_size_h(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	await callback.message.bot.edit_message_text(
		l10n.format_value("ask-for-item-full-price"),
		reply_markup=cancel_ikb(l10n),
		chat_id=callback.message.chat.id,
		message_id=state_data.get("shop_message_id")
	)
	await state.update_data(item_size=callback.data)
	await state.set_state(EditShopActions.CHOOSE_ITEM_FULL_PRICE)


@create_router.message(EditShopActions.CHOOSE_ITEM_FULL_PRICE)
async def ask_for_item_full_price_h(msg: types.message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	if not msg.text.isdigit():
		await msg.delete()
		await msg.answer(l10n.format_value("not-a-number"))
		return
	await msg.delete()
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-item-discount-price"),
		reply_markup=cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("shop_message_id")
	)
	await state.update_data(item_full_price=msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)


@create_router.message(EditShopActions.CHOOSE_ITEM_DISCOUNT_PRICE)
async def ask_for_item_discount_price_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	if not msg.text.isdigit():
		await msg.delete()
		await msg.answer(l10n.format_value("not-a-number"))
		return
	await msg.delete()
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-item-available-count"),
		reply_markup=cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("shop_message_id")
	)
	await state.update_data(item_discount_price=msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)


@create_router.message(EditShopActions.CHOOSE_ITEM_AVAILABLE_COUNT)
async def ask_for_item_available_count_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	if not msg.text.isdigit():
		await msg.delete()
		await msg.answer(l10n.format_value("not-a-number"))
		return
	await msg.delete()
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-item-in-stock"),
		reply_markup=yes_no_cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("shop_message_id")
	)
	await state.update_data(item_available_count=msg.text)
	await state.set_state(EditShopActions.CHOOSE_ITEM_IN_STOCK)


@create_router.callback_query(EditShopActions.CHOOSE_ITEM_IN_STOCK)
async def ask_for_item_in_stock_h(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	if callback.data == "btn_yes":
		await state.update_data(item_in_stock=True)
	else:
		await state.update_data(item_in_stock=False)
	await callback.bot.edit_message_text(
		l10n.format_value("ask-for-item-image"),
		reply_markup=cancel_ikb(l10n),
		chat_id=callback.message.chat.id,
		message_id=state_data.get("shop_message_id")
	)
	await state.set_state(EditShopActions.CHOOSE_ITEM_IMAGE)


@create_router.message(EditShopActions.CHOOSE_ITEM_IMAGE)
async def ask_for_item_image_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	if not msg.photo:
		await msg.delete()
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
			description=state_data.get("item_description"),
			image_path=str(save_location),
			size=state_data.get("item_size"),
			full_price=float(state_data.get("item_full_price")),
			discount_price=float(state_data.get("item_discount_price")),
			available_count=int(state_data.get("item_available_count")),
			in_stock=bool(state_data.get("item_in_stock")),
			category_id=int(state_data.get("category_id"))
		)
	await msg.delete()
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=state_data.get("shop_message_id"))
	await msg.answer(l10n.format_value("item-created"), reply_markup=edit_shop_kb(l10n))
	await state.clear()
	await state.set_state(EditShopActions.EDIT_SHOP)
