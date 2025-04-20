from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import or_f
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database.methods import get_users_by_full_name, get_user_by_telegram_id, add_event_privilege_grant, delete_event_privilege_grant, get_privilege_by_user
from database.enums import AdminPrivilege, EventPrivilege
from database import async_session
from filters import LocalizedTextFilter, PrivilegeFilter
from keyboards.common import admin_kb, cancel_kb
from keyboards.inline import user_event_privileges_ikb, names_ikb
from keyboards.callback_factories import EventPrivilegeButtonFactory, UserFactory
from state_machines.grant_event_privileges import GrantEventPrivilegesActions
from state_machines.admin import AdminActions

grant_event_privileges_router = Router()
grant_event_privileges_router.message.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_MODERATORS))
grant_event_privileges_router.callback_query.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_MODERATORS))


@grant_event_privileges_router.message(AdminActions.ADMIN_PANEL, LocalizedTextFilter("btn-give-event-privileges"))
async def handle_grant_event_privileges(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_grant_event_privileges")
	await msg.answer(l10n.format_value("ask-for-full-name"), reply_markup=cancel_kb(l10n))
	await state.set_state(GrantEventPrivilegesActions.WAIT_NAME)


@grant_event_privileges_router.message(or_f(
	GrantEventPrivilegesActions.WAIT_NAME,
	GrantEventPrivilegesActions.CHOOSE_USER,
	GrantEventPrivilegesActions.PRIVILEGES_KB
),
	LocalizedTextFilter("btn-cancel"))
async def handle_back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="back_to_menu")
	await msg.answer(l10n.format_value("hello-admin"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@grant_event_privileges_router.message(GrantEventPrivilegesActions.WAIT_NAME)
async def handle_user_full_username(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_user_full_username")
	async with async_session() as session:
		subjects = await get_users_by_full_name(session, msg.text.strip())
	if not subjects:
		await msg.answer(l10n.format_value("wrong-full-name"), reply_markup=cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("choose-name-from-list"), reply_markup=names_ikb(subjects))
	await state.set_state(GrantEventPrivilegesActions.CHOOSE_USER)


@grant_event_privileges_router.callback_query(GrantEventPrivilegesActions.CHOOSE_USER, UserFactory.filter())
async def handle_user_choise(callback: types.CallbackQuery, callback_data: UserFactory, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_user_full_username")
	async with async_session() as session:
		subject = await get_user_by_telegram_id(session, data.telegram_id)
	user_event_privileges = await user_event_privileges_ikb(l10n, subject.id)
	await callback.message.answer(
		l10n.format_value("user-privileges", args={"fullname": callback_data.full_name}),
		reply_markup=user_event_privileges)
	await callback.message.delete()
	await state.set_state(GrantEventPrivilegesActions.PRIVILEGES_KB)


@grant_event_privileges_router.callback_query(GrantEventPrivilegesActions.PRIVILEGES_KB, EventPrivilegeButtonFactory.filter())
async def handle_privileges_kb(callback: types.CallbackQuery, callback_data: EventPrivilegeButtonFactory, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_privileges_kb")
	async with async_session() as session:
		admin = await get_user_by_telegram_id(session, callback.from_user.id)
	if callback_data.grant_id is None:
		async with async_session() as session:
			await add_event_privilege_grant(
							session=session,
							user_id=callback_data.subject_id,
							privilege_id=admin.privileges_id,
							event_id=callback_data.event_id,
							privileges=EventPrivilege.CAN_GIVE_POINTS)
	else:
		async with async_session() as session:
			await delete_event_privilege_grant(session, callback_data.grant_id)
	user_event_privileges = await user_event_privileges_ikb(l10n, callback_data.subject_id)
	await callback.message.edit_reply_markup(
		reply_markup=user_event_privileges)
	await log.adebug("log-admin-action", action="handle_privileges_kb")
