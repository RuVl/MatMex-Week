from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from config import ADMIN_CHAT_ID
from database import async_session
from database.methods import create_user, create_apply, get_user_by_telegram_id, create_privilege
from database.models import User
from database.enums import AdminPrivilege
from filters import FullNameFilter
from keyboards.common import menu_kb, yes_no_kb, manual_check_kb
from keyboards.inline import verification_request_ikb
from state_machines.registration import RegistrationsActions
from utils import escape_md_v2
from env import TelegramKeys

register_router = Router()


@register_router.message(CommandStart(deep_link=False), flags={'chat_action': True})
async def start_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, cached_user: User):
	if cached_user is None:
		await msg.answer(l10n.format_value("hi"), reply_markup=ReplyKeyboardRemove())
		await msg.answer(l10n.format_value("ask-name"))
		await msg.answer(l10n.format_value("tell-about-pc"))

		await state.set_state(RegistrationsActions.NAME_WAITING)
	else:
		menu = await menu_kb(l10n, msg.from_user.id)
		await msg.answer(l10n.format_value("hi-user", args={
			'fullname': escape_md_v2(cached_user.full_name),
		}), reply_markup=menu)
		await state.clear()


@register_router.message(RegistrationsActions.NAME_WAITING, flags={'chat_action': True})
async def correct_fullname_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	if not await FullNameFilter().__call__(msg):
		await msg.answer(l10n.format_value("wrong-name"))
		return

	fullname = msg.text.strip()
	await log.ainfo("creating-new-user", full_name=fullname)

	async with async_session() as session:
		user = await create_user(session, msg.from_user.id, msg.from_user.username, fullname)
		if str(msg.from_user.id) in TelegramKeys.ADMINS:
			await create_privilege(session = session, user_id = user.id, privilege_mask=AdminPrivilege.ALL, provider_id=None)
	await msg.answer(l10n.format_value("thanks-name-html", args={
		'fullname': escape_md_v2(fullname)
	}), parse_mode=ParseMode.HTML)
	await msg.answer(l10n.format_value("ask-pc"), reply_markup=yes_no_kb(l10n))

	await state.set_state(RegistrationsActions.CHECK_MEMBER)

@register_router.message(RegistrationsActions.CHECK_MEMBER, flags={'chat_action': True})
async def handle_in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	answer = msg.text.strip()

	if answer == l10n.format_value('btn-yes'):
		await msg.answer(l10n.format_value("send-for-manual-check"), reply_markup=manual_check_kb(l10n))
		await state.set_state(RegistrationsActions.MANUAL_MEMBER_CHECK)
	elif answer == l10n.format_value('btn-no'):
		menu = await menu_kb(l10n, msg.from_user.id)
		await msg.answer(l10n.format_value("ask-to-join"), reply_markup=menu)
		await state.clear()  # end
	else:
		await msg.answer(l10n.format_value("ask-valid-answer"), reply_markup=yes_no_kb(l10n))


@register_router.message(RegistrationsActions.MANUAL_MEMBER_CHECK, flags={'chat_action': True})
async def handle_manual_check_confirm(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	answer = msg.text.strip()

	if answer == l10n.format_value('btn-send-for-check'):
		async with async_session() as session:
			user = await get_user_by_telegram_id(session, msg.from_user.id)  # do not user cache
			apply = await create_apply(session, user.id)

		await log.ainfo("created-apply-for-check", apply_id=apply.id, user_id=user.id, fullname=user.full_name)
		await msg.bot.send_message(ADMIN_CHAT_ID, l10n.format_value("apply-check", args={
			'status': apply.status,
			'fullname': escape_md_v2(user.full_name),
			'username': escape_md_v2(user.telegram_username),
			'verified_by': None
		}), reply_markup=verification_request_ikb(l10n, apply_id=apply.id))
		menu = await menu_kb(l10n, msg.from_user.id)
		await msg.answer(l10n.format_value("wait-until-checked"), reply_markup=menu)
		await state.clear()  # end
	elif answer == l10n.format_value('btn-just-kidding'):
		menu = await menu_kb(l10n, msg.from_user.id)
		await msg.answer(l10n.format_value("ask-to-join"), reply_markup=menu)
		await state.clear()  # end
	else:
		await msg.answer(l10n.format_value("ask-valid-answer"), reply_markup=manual_check_kb(l10n))
