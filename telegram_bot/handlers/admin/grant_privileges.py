from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.enums import AdminPrivilege
from database.methods import add_privilege, create_privilege, get_privilege_by_user, get_user_by_telegram_id, get_users_by_full_name, is_provider_to, remove_privilege
from filters import LocalizedTextFilter, PrivilegeFilter
from keyboards.callback_factories import PrivilegeButtonFactory, UserFactory
from keyboards.common import admin_kb, cancel_kb
from keyboards.inline import names_ikb, user_rights_ikb
from state_machines.admin import AdminActions
from state_machines.grant_privileges import GrantPrivilegesActions

grant_privileges_router = Router()
grant_privileges_router.message.filter(
	PrivilegeFilter(AdminPrivilege.GRANT_PRIVILEGES)
)
grant_privileges_router.callback_query.filter(
	PrivilegeFilter(AdminPrivilege.GRANT_PRIVILEGES)
)


@grant_privileges_router.message(AdminActions.ADMIN_PANEL, LocalizedTextFilter("btn-give-rights"))
async def handle_grant_privileges(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="open_admin_panel")
	await msg.answer(l10n.format_value("ask-for-full-name"), reply_markup=cancel_kb(l10n))
	await state.set_state(GrantPrivilegesActions.WAIT_NAME)


@grant_privileges_router.message(
	or_f(
		GrantPrivilegesActions.WAIT_NAME,
		GrantPrivilegesActions.CHOOSE_USER,
		GrantPrivilegesActions.PRIVILEGES_KB
	),
	LocalizedTextFilter("btn-cancel")
)
async def back_to_menu_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="back_to_menu")
	await msg.answer(l10n.format_value("hello-admin"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@grant_privileges_router.message(GrantPrivilegesActions.WAIT_NAME)
async def user_full_username_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_user_full_username")
	async with async_session() as session:
		subjects = await get_users_by_full_name(session, msg.text.strip())
	if not subjects:
		await msg.answer(l10n.format_value("wrong-full-name"), reply_markup=cancel_kb(l10n))
		return
	await msg.answer(l10n.format_value("choose-name-from-list"), reply_markup=names_ikb(subjects))
	await state.set_state(GrantPrivilegesActions.CHOOSE_USER)


@grant_privileges_router.callback_query(GrantPrivilegesActions.CHOOSE_USER, UserFactory.filter())
async def user_choice_h(callback: types.CallbackQuery, callback_data: UserFactory, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	async with async_session() as session:
		subject = await get_user_by_telegram_id(session, callback_data.telegram_id)
		admin = await get_user_by_telegram_id(session, callback.from_user.id)

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
		l10n.format_value("user-privileges", args={"fullname": callback_data.full_name}),
		reply_markup=user_rights_ikb(l10n, admin_privileges.privilege, subject_privileges.privilege, admin.id, subject.id))
	await callback.message.delete()
	await state.set_state(GrantPrivilegesActions.PRIVILEGES_KB)


@grant_privileges_router.callback_query(GrantPrivilegesActions.PRIVILEGES_KB, PrivilegeButtonFactory.filter())
async def privileges_kb_h(callback: types.CallbackQuery, callback_data: PrivilegeButtonFactory, l10n: FluentLocalization, log: FilteringBoundLogger):
	if callback_data.admin_id == callback_data.subject_id:
		await callback.answer(l10n.format_value("cant-change-privileges-of-yourself"))
		return

	async with async_session() as session:
		admin_privileges = await get_privilege_by_user(session, callback_data.admin_id)
		subject_privileges = await get_privilege_by_user(session, callback_data.subject_id)
		can_grant = await is_provider_to(session, admin_privileges.id, subject_privileges.id)

	if not can_grant:
		await callback.answer(l10n.format_value("cant-change-privileges"), reply_markup=admin_kb(l10n))
		return

	if not callback_data.granted:
		async with async_session() as session:
			subject_privileges = await add_privilege(session, callback_data.subject_id, callback_data.privilege)
	else:
		async with async_session() as session:
			subject_privileges = await remove_privilege(session, callback_data.subject_id, callback_data.privilege)

	await callback.answer(str(subject_privileges.privilege))
	await callback.message.edit_reply_markup(
		reply_markup=user_rights_ikb(l10n, admin_privileges.privilege,
		                             subject_privileges.privilege, callback_data.admin_id, callback_data.subject_id)
	)
