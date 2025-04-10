from aiogram import F
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from handlers.utils import logger, get_user_context
from keyboards.common import get_category_kb, get_menu_kb
from state_machines.states_purchases import PurchasesActions

shop_router = Router()


@shop_router.message(F.text == 'Магазин')
async def handle_shop_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_shop_button")

	text = l10n.format_value("shop_hello")

	image_from_pc = FSInputFile(MEDIA_DIR / "shop_mock.jpg")
	await msg.answer_photo(
		image_from_pc,
		caption=text,
		parse_mode=ParseMode.HTML,
		reply_markup=get_category_kb(l10n)
	)
	await state.set_state(PurchasesActions.CHOOSE_CATEGORY)

	log.info("log-state-changed", state=PurchasesActions.CHOOSE_CATEGORY.state)
	log.info("log-handler-completed")


@shop_router.message(PurchasesActions.CHOOSE_CATEGORY, F.text == 'Отмена')
async def handle_shop_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_shop_cancel")

	text = l10n.format_value("cancel_message")

	await msg.answer(
		text,
		reply_markup=get_menu_kb(l10n)
	)
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")


@shop_router.message(PurchasesActions.CHOOSE_CATEGORY, or_f(F.text == 'Шопперы', F.text == 'Футболки'))
async def handle_shop_category(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_shop_category", category=msg.text)

	# todo сделать select-запрос и выяснить какие футболки есть и сколько
	shirts_types = ['Матмех', 'Изоклины', 'Тетрис']  # todo select

	await msg.answer(l10n.format_value("shirts-type") + str(shirts_types))
	# todo сделать новое состояние с новой клавой и отменой
	await state.set_state(PurchasesActions.CHOOSE_PRODUCT)

	log.info("log-state-changed", state=PurchasesActions.CHOOSE_PRODUCT.state)
	log.info("log-handler-completed")
