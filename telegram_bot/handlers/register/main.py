from aiogram import F
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import create_user
from filters import FIOFilter, IsNotRegisteredFilter
from keyboards import get_menu_keyboard
from keyboards import get_yes_no_kb, manual_check_kb
from state_machines.states_registration import RegistrationsActions

register_router = Router()
register_router.message.filter(
	F.text
)


@register_router.message(CommandStart(),
                         IsNotRegisteredFilter())
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("hi"), reply_markup=ReplyKeyboardRemove())
	await msg.answer(l10n.format_value("ask-name"))
	await msg.answer(l10n.format_value("talk-about-pc"))
	await state.set_state(RegistrationsActions.NAME_WAITING)


@register_router.message(CommandStart())
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("hi"), reply_markup=get_menu_keyboard())
	await state.clear()

@register_router.message(RegistrationsActions.NAME_WAITING,
                         FIOFilter())
async def input_FIO(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("thanks-FIO") + ", " + msg.text.strip() + "\\!")
	async with async_session() as session:
		await create_user(session, msg.from_user.id, msg)
	await msg.answer(l10n.format_value("ask-pc"), reply_markup=get_yes_no_kb())
	await state.set_state(RegistrationsActions.CHECK_MEMBER)


@register_router.message(RegistrationsActions.NAME_WAITING)
async def wrong_FIO_format(msg: types.Message, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("wrong-FIO"))


@register_router.message(RegistrationsActions.CHECK_MEMBER,
                         F.text == 'Да')
async def in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("send-for-manual-check"), reply_markup=manual_check_kb())  # todo отправить на ручную проверку
	await state.set_state(RegistrationsActions.MANUAL_MEMBER_CHECK)


@register_router.message(RegistrationsActions.CHECK_MEMBER,
                         F.text == 'Нет')
async def not_in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-to-join"), reply_markup=get_menu_keyboard())  # todo зарегистрировать
	await state.clear()


@register_router.message(RegistrationsActions.MANUAL_MEMBER_CHECK,
                         F.text == 'Отправить на ручную проверку')
async def sent_for_manual_check(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("wait-until-checked"), reply_markup=get_menu_keyboard())  # todo зарегистрировать
	await state.clear()


@register_router.message(RegistrationsActions.MANUAL_MEMBER_CHECK,
                         F.text == 'Нет, я пошутил')
async def sent_for_manual_check(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-to-join"), reply_markup=get_menu_keyboard())  # todo зарегистрировать
	await state.clear()
