from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import or_f
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database.methods import get_privilege_by_user, get_users_by_full_name, create_privilege, get_user_by_telegram_id, add_privilege, remove_privilege, is_provider_to
from database.enums import AdminPrivilege
from database import async_session
from filters import LocalizedTextFilter, PrivilegeFilter
from keyboards.common import admin_kb, cancel_kb
from keyboards.inline import user_rights_ikb, names_ikb
from keyboards.callback_factories import PrivilegeButtonFactory, UserFactory
from state_machines.grant_privileges import GrantPrivilegesActions
from state_machines.admin import AdminActions

grant_privileges_router = Router()
grant_privileges_router.message.filter(
	PrivilegeFilter(AdminPrivilege.GRANT_PRIVILEGES))
grant_privileges_router.callback_query.filter(
	PrivilegeFilter(AdminPrivilege.GRANT_PRIVILEGES))


@grant_privileges_router.message(AdminActions.ADMIN_PANEL, LocalizedTextFilter("btn-give-rights"))
async def handle_grant_privileges(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="open_admin_panel")
	await msg.answer(l10n.format_value("ask-for-full-name"), reply_markup=cancel_kb(l10n))
	await state.set_state(GrantPrivilegesActions.WAIT_NAME)


@grant_privileges_router.message(or_f(
	GrantPrivilegesActions.WAIT_NAME,
	GrantPrivilegesActions.CHOOSE_USER,
	GrantPrivilegesActions.PRIVILEGES_KB
),
	LocalizedTextFilter("btn-cancel"))
async def handle_back_to_menu(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="back_to_menu")
	await msg.answer(l10n.format_value("hello-admin"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@grant_privileges_router.message(GrantPrivilegesActions.WAIT_NAME)
async def handle_user_full_username(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_user_full_username")
	async with async_session() as session:
		subjects = await get_users_by_full_name(session, msg.text.strip())
	if not subjects:
		await msg.answer(l10n.format_value("wrong-full-name"), reply_markup=cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("choose-name-from-list"), reply_markup=names_ikb(subjects))
	await state.set_state(GrantPrivilegesActions.CHOOSE_USER)


@grant_privileges_router.callback_query(GrantPrivilegesActions.CHOOSE_USER, UserFactory.filter())
async def handle_user_choise(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_user_full_username")
	data = UserFactory.unpack(callback.data)
	async with async_session() as session:
		subject = await get_user_by_telegram_id(session, data.telegram_id)
		admin = await get_user_by_telegram_id(session, callback.from_user.id)
	if subject.id == admin.id:
		await callback.answer(l10n.format_value("cant-change-privileges-of-yourself"))
		return

	async with async_session() as session:
		admin_privileges = await get_privilege_by_user(session, admin.id)
		subject_privileges = await get_privilege_by_user(session, subject.id)
		if not subject_privileges:
			subject_privileges = await create_privilege(session=session, user_id=subject.id, privilege_mask=0, provider_id=admin_privileges.id)
		can_grant = await is_provider_to(session, admin_privileges.id, subject_privileges.id)

	if not can_grant:
		await callback.message.answer(l10n.format_value("cant-change-privileges"), reply_markup=admin_kb(l10n))
		return

	await callback.message.answer(
		l10n.format_value("user-privileges") + callback.message.text,
		reply_markup=user_rights_ikb(l10n, admin_privileges.privilege, subject_privileges.privilege, admin.id, subject.id))
	await callback.message.delete()
	await state.set_state(GrantPrivilegesActions.PRIVILEGES_KB)


@grant_privileges_router.callback_query(GrantPrivilegesActions.PRIVILEGES_KB, PrivilegeButtonFactory.filter())
async def handle_privileges_kb(callback: types.CallbackQuery, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_privileges_kb")
	data = PrivilegeButtonFactory.unpack(callback.data)
	if data.admin_id == data.subject_id:
		await callback.answer(l10n.format_value("cant-change-privileges-of-yourself"))
		return

	if not data.granted:
		async with async_session() as session:
			await add_privilege(session, data.subject_id, data.privilege)
	else:
		async with async_session() as session:
			await remove_privilege(session, data.subject_id, data.privilege)

	async with async_session() as session:
		admin_privileges = await get_privilege_by_user(session, data.admin_id)
		subject_privileges = await get_privilege_by_user(session, data.subject_id)
		can_grant = await is_provider_to(session, admin_privileges.id, subject_privileges.id)

	if not can_grant:
		await callback.answer(l10n.format_value("cant-change-privileges"), reply_markup=admin_kb(l10n))
		return

	await callback.answer(str(subject_privileges.privilege))
	await callback.message.edit_reply_markup(
		reply_markup=user_rights_ikb(l10n, admin_privileges.privilege, subject_privileges.privilege, data.admin_id, data.subject_id))
	await log.adebug("log-admin-action", action="handle_privileges_kb")
