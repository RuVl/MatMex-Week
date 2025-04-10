from aiogram import F
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import create_user
from filters import FullNameFilter, IsNotRegisteredFilter
from handlers.typing import send_typing
from handlers.utils import logger, get_user_context
from keyboards.common import get_menu_kb, get_yes_no_kb, manual_check_kb
from state_machines.states_registration import RegistrationsActions

register_router = Router()


@register_router.message(CommandStart(deep_link=False), IsNotRegisteredFilter())
async def handle_start_unregistered(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_start_unregistered")

	async with send_typing(msg) as m:
		await m.answer(l10n.format_value("hi"), reply_markup=ReplyKeyboardRemove())
		await m.answer(l10n.format_value("ask-name"))
		await m.answer(l10n.format_value("talk-about-pc"))

	await state.set_state(RegistrationsActions.NAME_WAITING)

	log.info("log-state-changed", state=RegistrationsActions.NAME_WAITING.state)
	log.info("log-handler-completed")


@register_router.message(CommandStart(deep_link=False))
async def handle_start_registered(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_start_registered")

	await msg.answer(l10n.format_value("hi"), reply_markup=get_menu_kb(l10n))
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")


@register_router.message(RegistrationsActions.NAME_WAITING, FullNameFilter())
async def handle_input_fullname(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_input_fullname", fullname=msg.text.strip())

	async with async_session() as session:
		await create_user(session, msg.from_user.id, msg.text.strip())

	async with send_typing(msg) as m:
		await m.answer(l10n.format_value("thanks-name") + ", " + msg.text.strip() + r'\!')
		await m.answer(l10n.format_value("ask-pc"), reply_markup=get_yes_no_kb(l10n))

	await state.set_state(RegistrationsActions.CHECK_MEMBER)

	log.info("log-state-changed", state=RegistrationsActions.CHECK_MEMBER.state)
	log.info("log-handler-completed")


@register_router.message(RegistrationsActions.NAME_WAITING)
async def handle_wrong_name_format(msg: types.Message, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_wrong_name_format", text=msg.text)

	await msg.answer(l10n.format_value("wrong-name"))

	log.info("log-handler-completed")


@register_router.message(RegistrationsActions.CHECK_MEMBER, F.text == 'Да')
async def handle_in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_in_pc")

	await msg.answer(l10n.format_value("send-for-manual-check"), reply_markup=manual_check_kb(l10n))  # todo отправить на ручную проверку
	await state.set_state(RegistrationsActions.MANUAL_MEMBER_CHECK)

	log.info("log-state-changed", state=RegistrationsActions.MANUAL_MEMBER_CHECK.state)
	log.info("log-handler-completed")


@register_router.message(RegistrationsActions.CHECK_MEMBER, F.text == 'Нет')
async def handle_not_in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_not_in_pc")

	await msg.answer(l10n.format_value("ask-to-join"), reply_markup=get_menu_kb(l10n))  # todo зарегистрировать
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")


@register_router.message(RegistrationsActions.MANUAL_MEMBER_CHECK, F.text == 'Отправить на ручную проверку')
async def handle_manual_check_confirm(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_manual_check_confirm")

	await msg.answer(l10n.format_value("wait-until-checked"), reply_markup=get_menu_kb(l10n))  # todo зарегистрировать
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")


@register_router.message(RegistrationsActions.MANUAL_MEMBER_CHECK, F.text == 'Нет, я пошутил')
async def handle_manual_check_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_manual_check_cancel")

	await msg.answer(l10n.format_value("ask-to-join"), reply_markup=get_menu_kb(l10n))  # todo зарегистрировать
	await state.clear()

	log.info("log-state-changed", state="cleared")
	log.info("log-handler-completed")
