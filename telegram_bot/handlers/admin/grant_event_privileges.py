from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.enums import AdminPrivilege, EventPrivilege
from database.methods import add_event_privilege_grant, delete_event_privilege_grant, get_user_by_telegram_id, get_users_by_full_name
from filters import LocalizedTextFilter, PrivilegeFilter
from keyboards.callback_factories import EventPrivilegeButtonFactory, UserFactory
from keyboards.common import admin_kb, cancel_kb
from keyboards.inline import names_ikb, user_event_privileges_ikb
from state_machines.admin import AdminActions
from state_machines.grant_event_privileges import GrantEventPrivilegesActions

grant_event_privileges_router = Router()
grant_event_privileges_router.message.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_MODERATORS))
grant_event_privileges_router.callback_query.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_MODERATORS))


@grant_event_privileges_router.message(AdminActions.ADMIN_PANEL, LocalizedTextFilter("btn-give-event-privileges"))
async def grant_event_privileges_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-full-name"), reply_markup=cancel_kb(l10n))
	await state.set_state(GrantEventPrivilegesActions.WAIT_NAME)


@grant_event_privileges_router.message(or_f(
	GrantEventPrivilegesActions.WAIT_NAME,
	GrantEventPrivilegesActions.CHOOSE_USER,
	GrantEventPrivilegesActions.PRIVILEGES_KB
),
	LocalizedTextFilter("btn-cancel"))
async def back_to_menu_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("hello-admin"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@grant_event_privileges_router.message(GrantEventPrivilegesActions.WAIT_NAME)
async def user_full_username_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	async with async_session() as session:
		subjects = await get_users_by_full_name(session, msg.text.strip())
	if not subjects:
		await msg.answer(l10n.format_value("wrong-full-name"), reply_markup=cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("choose-name-from-list"), reply_markup=names_ikb(subjects))
	await state.set_state(GrantEventPrivilegesActions.CHOOSE_USER)


@grant_event_privileges_router.callback_query(GrantEventPrivilegesActions.CHOOSE_USER, UserFactory.filter())
async def user_choice_h(callback: types.CallbackQuery, callback_data: UserFactory, state: FSMContext, l10n: FluentLocalization):
	async with async_session() as session:
		subject = await get_user_by_telegram_id(session, callback_data.telegram_id)

	user_event_privileges = await user_event_privileges_ikb(l10n, subject.id)
	await callback.message.answer(
		l10n.format_value("user-privileges", args={"fullname": subject.full_name}),
		reply_markup=user_event_privileges)

	await callback.message.delete()
	await state.set_state(GrantEventPrivilegesActions.PRIVILEGES_KB)


@grant_event_privileges_router.callback_query(GrantEventPrivilegesActions.PRIVILEGES_KB, EventPrivilegeButtonFactory.filter())
async def privileges_kb_h(callback: types.CallbackQuery, callback_data: EventPrivilegeButtonFactory, l10n: FluentLocalization):
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
