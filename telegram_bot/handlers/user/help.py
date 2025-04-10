from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from handlers.utils import localized_text_filter, logger, get_user_context
from keyboards.common import get_menu_kb, get_cancel_kb
from state_machines.states_help import HelpActions

support_router = Router()


@support_router.message(F.text.func(localized_text_filter("btn-support")))
async def handle_support_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_support_button")

	await msg.answer(l10n.format_value("helping"), reply_markup=get_cancel_kb(l10n))
	await state.set_state(HelpActions.MESSAGE_OR_CANCEL)

	log.info("log-state-changed", state=HelpActions.MESSAGE_OR_CANCEL.state)
	log.info("log-handler-completed")


@support_router.message(HelpActions.MESSAGE_OR_CANCEL, F.text.func(localized_text_filter("btn-cancel")))
async def handle_support_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_support_cancel")

	await msg.answer(l10n.format_value("cancel_message"), reply_markup=get_menu_kb(l10n))
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")


@support_router.message(HelpActions.MESSAGE_OR_CANCEL)
async def handle_support_message(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_support_message", text=msg.text)

	# user_question = msg.text
	# user_id = msg.from_user.id
	# TODO отправить в чат админов
	await msg.answer(l10n.format_value("send_helping"), reply_markup=get_menu_kb(l10n))
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")
