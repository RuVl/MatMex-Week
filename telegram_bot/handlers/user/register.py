from aiogram import F
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.methods import create_user
from database.models import User
from filters import FullNameFilter
from handlers.typing import send_typing, with_typing
from keyboards.common import get_menu_kb, get_yes_no_kb, manual_check_kb
from state_machines.states_registration import RegistrationsActions

register_router = Router()


@with_typing
@register_router.message(CommandStart(deep_link=False))
async def start_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger, cached_user: User):
	if cached_user is None:
		await msg.answer(l10n.format_value("hi"), reply_markup=ReplyKeyboardRemove())
		await msg.answer(l10n.format_value("ask-name"))
		await msg.answer(l10n.format_value("tell-about-pc"))

		await state.set_state(RegistrationsActions.NAME_WAITING)
		await log.ainfo("state-changed", state=RegistrationsActions.NAME_WAITING.state)
	else:
		await msg.answer(l10n.format_value("hi"), reply_markup=get_menu_kb(l10n))
		await state.clear()
		await log.ainfo("state-changed", state="cleared")


@register_router.message(RegistrationsActions.NAME_WAITING, FullNameFilter())
async def correct_fullname_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	telegram_id = msg.from_user.id
	fullname = msg.text.strip()

	await log.ainfo("Creating new user", telegram_id=telegram_id, full_name=fullname)
	async with async_session() as session:
		await create_user(session, telegram_id, fullname)

	async with send_typing(msg) as m:
		await m.answer(l10n.format_value("thanks-name") + ", " + msg.text.strip() + r'\!')
		await m.answer(l10n.format_value("ask-pc"), reply_markup=get_yes_no_kb(l10n))

	await state.set_state(RegistrationsActions.CHECK_MEMBER)
	await log.adebug("state-changed", state=RegistrationsActions.CHECK_MEMBER.state)


@register_router.message(RegistrationsActions.NAME_WAITING, FullNameFilter())
async def wrong_fullname_h(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	await msg.answer(l10n.format_value("wrong-name"))
	await log.adebug("handler-completed")


@register_router.message(RegistrationsActions.CHECK_MEMBER, F.text == 'Да')
async def handle_in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await msg.answer(l10n.format_value("send-for-manual-check"), reply_markup=manual_check_kb(l10n))  # todo отправить на ручную проверку
	await state.set_state(RegistrationsActions.MANUAL_MEMBER_CHECK)
	await log.adebug("state-changed", state=RegistrationsActions.MANUAL_MEMBER_CHECK.state)


@register_router.message(RegistrationsActions.CHECK_MEMBER, F.text == 'Нет')
async def handle_not_in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await msg.answer(l10n.format_value("ask-to-join"), reply_markup=get_menu_kb(l10n))  # todo зарегистрировать
	await state.clear()
	await log.adebug("state-changed", state="cleared")


@register_router.message(RegistrationsActions.MANUAL_MEMBER_CHECK, F.text == 'Отправить на ручную проверку')
async def handle_manual_check_confirm(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await msg.answer(l10n.format_value("wait-until-checked"), reply_markup=get_menu_kb(l10n))  # todo зарегистрировать
	await state.clear()
	await log.adebug("state-changed", state="cleared")


@register_router.message(RegistrationsActions.MANUAL_MEMBER_CHECK, F.text == 'Нет, я пошутил')
async def handle_manual_check_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await msg.answer(l10n.format_value("ask-to-join"), reply_markup=get_menu_kb(l10n))  # todo зарегистрировать
	await state.clear()
	await log.adebug("state-changed", state="cleared")
