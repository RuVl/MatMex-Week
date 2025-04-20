from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization
from datetime import datetime

from database.enums import AdminPrivilege
from database.models import User, EventPrivilegeGrant
from database.methods import get_user_event_grants, get_active_events, get_all_events
from database import async_session
from keyboards.callback_factories import PKApplyFactory, PrivilegeButtonFactory, UserFactory, EventPrivilegeButtonFactory, EventToGrantFactory

def verification_request_ikb(l10n: FluentLocalization, apply_id: int) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.row(
		InlineKeyboardButton(
			text=l10n.format_value("btn-approve-apply"),
			callback_data=PKApplyFactory(
				apply_id=apply_id, decision='approve').pack()
		),
		InlineKeyboardButton(
			text=l10n.format_value("btn-decline-apply"),
			callback_data=PKApplyFactory(
				apply_id=apply_id, decision='reject').pack()
		),
	)
	return builder.as_markup()


def verified_request_ikb(l10n: FluentLocalization, apply_id: int) -> InlineKeyboardMarkup:
	return InlineKeyboardMarkup(inline_keyboard=[[
		InlineKeyboardButton(
			text=l10n.format_value("btn-review-apply"),
			callback_data=PKApplyFactory(
				apply_id=apply_id, decision='review').pack()
		)
	]])


privilege_names = dict([
	[AdminPrivilege.GRANT_PRIVILEGES, "privilege-grant-privileges"],
	[AdminPrivilege.EDIT_PROMOCODES, "privilege-edit-promocodes"],
	[AdminPrivilege.EDIT_SHOP, "privilege-edit-shop"],
	[AdminPrivilege.EDIT_EVENTS, "privilege-edit-events"],
	[AdminPrivilege.EDIT_PK_APPLY, "privilege-edit-pk-apply"],
	[AdminPrivilege.EDIT_MODERATORS, "privilege-edit-moderators"],
])


def user_rights_ikb(l10n: FluentLocalization, admin_rights: int, user_rigts: int, admin_id: int, subject_id: int) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for privilege in AdminPrivilege:
		if privilege.value & admin_rights:
			builder.row(
				InlineKeyboardButton(
					text=l10n.format_value(privilege_names[privilege.value]),
					callback_data=PrivilegeButtonFactory(
						privilege=privilege.value,
						granted=bool(privilege.value & user_rigts),
						admin_id=admin_id,
						subject_id=subject_id).pack()
				),
				InlineKeyboardButton(
					text=l10n.format_value(
						"btn-emoji-yes" if privilege.value & user_rigts else "btn-emoji-no"),
					callback_data=PrivilegeButtonFactory(
						privilege=privilege.value,
						granted=bool(privilege.value & user_rigts),
						admin_id=admin_id,
						subject_id=subject_id).pack()
				),
			)
	return builder.as_markup()


def names_ikb(users: list[User]):
	builder = InlineKeyboardBuilder()
	for user in users:
		data = UserFactory(
			full_name=user.full_name,
			telegram_id=user.telegram_id,
			telegram_username=user.telegram_username).pack()
		builder.row(InlineKeyboardButton(
			text=f"{user.full_name} : {user.telegram_username}",
			callback_data=data,
		))
	return builder.as_markup()

async def user_event_privileges_ikb(l10n: FluentLocalization, subject_id: int) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	async with async_session() as session:
		subject_event_grants = await get_user_event_grants(session, subject_id)
		all_events = await get_all_events(session)
	for event in all_events:
		grant_id = None
		for event_grant in subject_event_grants:
			if event_grant.event_id == event.id:
				grant_id = event_grant.id
				break
		builder.row(
		InlineKeyboardButton(
			text=event.name,
			callback_data=EventPrivilegeButtonFactory(
				event_id=event.id,
				grant_id=grant_id,
				subject_id=subject_id).pack()
		),
		InlineKeyboardButton(
			text=l10n.format_value("btn-emoji-yes" if grant_id is not None else "btn-emoji-no"),
			callback_data=EventPrivilegeButtonFactory(
				event_id=event.id,
				grant_id=grant_id,
				subject_id=subject_id).pack()
		),
	)
  
	return builder.as_markup()

async def active_events_ikb(l10n: FluentLocalization, event_grants: list[EventPrivilegeGrant], subject_id : int, admin_tg_id : int) -> InlineKeyboardMarkup | None:
	active_events = []
	async with async_session() as session:
		all_events = await get_active_events(session)

	for event in all_events:
		for grant in event_grants:
			if grant.event_id == event.id:
				active_events.append((event, grant))
	if not active_events:
		return None

	builder = InlineKeyboardBuilder()
	for event_pair in active_events:
		builder.row(
			InlineKeyboardButton(
				text=event_pair[0].name,
				callback_data=EventToGrantFactory(
					event_id=event_pair[0].id,
					grant_id=event_pair[1].id,
					subject_id = subject_id,
     				admin_tg_id = admin_tg_id
				).pack()
			),
		)
	return builder.as_markup()
