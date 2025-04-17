from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization

from database.enums import AdminPrivilege
from database.models import User
from keyboards.callback_factories import PKApplyFactory, PrivilegeButtonFactory, UserFactory

def verification_request_ikb(l10n: FluentLocalization, apply_id: int) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	builder.row(
		InlineKeyboardButton(
			text=l10n.format_value("btn-approve-apply"),
			callback_data=PKApplyFactory(apply_id=apply_id, decision='approve').pack()
		),
		InlineKeyboardButton(
			text=l10n.format_value("btn-decline-apply"),
			callback_data=PKApplyFactory(apply_id=apply_id, decision='reject').pack()
		),
	)
	return builder.as_markup()


def verified_request_ikb(l10n: FluentLocalization, apply_id: int) -> InlineKeyboardMarkup:
	return InlineKeyboardMarkup(inline_keyboard=[[
		InlineKeyboardButton(
			text=l10n.format_value("btn-review-apply"),
			callback_data=PKApplyFactory(apply_id=apply_id, decision='review').pack()
		)
	]])

privilege_names = dict([
	[AdminPrivilege.GRANT_PRIVELEGES.value, "privilege-grant-privileges"],
	[AdminPrivilege.EDIT_PROMOCODES.value, "privilege-edit-promocodes"],
	[AdminPrivilege.EDIT_SHOP.value, "privilege-edit-shop"],
	[AdminPrivilege.EDIT_EVENTS.value, "privilege-edit-events"],
	[AdminPrivilege.EDIT_PK_APPLY.value, "privilege-edit-pk-apply"],
	[AdminPrivilege.EDIT_MODERATORS.value, "privilege-edit-moderators"],
])

def user_rights_ikb(l10n: FluentLocalization, admin_rights : int, user_rigts : int, admin_id : int, subject_id : int) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	for privilege in AdminPrivilege:
		if privilege.value & admin_rights:
			builder.row(
				InlineKeyboardButton(
					text=l10n.format_value(privilege_names[privilege.value]),
					callback_data=PrivilegeButtonFactory(
         												privilege = privilege.value, 
                     									granted = bool(privilege.value & user_rigts), 
                              							admin_id = admin_id,
                                     					subject_id = subject_id).pack()
				),
				InlineKeyboardButton(
					text=l10n.format_value("btn-emoji-yes" if privilege.value & user_rigts else "btn-emoji-no"),
					callback_data=PrivilegeButtonFactory(
         												privilege = privilege.value, 
                     									granted = bool(privilege.value & user_rigts), 
                              							admin_id = admin_id,
                                     					subject_id = subject_id).pack()
				),
			)
	return builder.as_markup()

def names_ikb(users : list[User]):
	builder = InlineKeyboardBuilder()
	for user in users:
		data = UserFactory(
						full_name = user.full_name, 
						telegram_id = user.telegram_id,
						telegram_username = user.telegram_username).pack()
		builder.row(InlineKeyboardButton(
										text= user.full_name + " : " + user.telegram_username,
										callback_data=data,
										))
	return builder.as_markup()