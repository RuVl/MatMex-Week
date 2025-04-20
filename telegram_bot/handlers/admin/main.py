from aiogram import F, Router, types
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.enums import AdminPrivilege, ApplyStatus
from database.methods import update_apply_status
from database.models import User
from filters import FromBotToAdminFilter, PrivilegeFilter
from keyboards.callback_factories import PKApplyFactory, SupportFactory
from keyboards.inline import verification_request_ikb, verified_request_ikb
from utils import escape_md_v2
from .admin_menu import admin_menu_router

admin_router = Router()  # TODO Check privileges
admin_router.include_routers(admin_menu_router)


@admin_router.message(FromBotToAdminFilter(),
	F.reply_to_message.text.split("\n")[-1].startswith(SupportFactory.__prefix__)
)
async def handle_send_support(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="send_support")
	original = msg.reply_to_message
	data = SupportFactory.unpack(original.text.split('\n')[-1])
	await msg.bot.send_message(chat_id=data.user_id, text=msg.text, reply_to_message_id=data.message_id)
	await msg.answer(l10n.format_value("support-sent"))


@admin_router.callback_query(PKApplyFactory.filter(), PrivilegeFilter(AdminPrivilege.EDIT_PK_APPLY))
async def apply_verify(clb: CallbackQuery, callback_data: PKApplyFactory, l10n: FluentLocalization, log: FilteringBoundLogger, cached_user: User):
	match callback_data.decision:
		case 'approve':
			await log.adebug("log-admin-action", action="approve-apply", apply_id=callback_data.apply_id)
			status = ApplyStatus.APPROVED
			verified_by = cached_user.full_name
		case 'reject':
			await log.adebug("log-admin-action", action="reject-apply", apply_id=callback_data.apply_id)
			status = ApplyStatus.REJECTED
			verified_by = cached_user.full_name
		case 'review':
			await log.adebug("log-admin-action", action="rollback-apply", apply_id=callback_data.apply_id)
			status = ApplyStatus.PENDING
			verified_by = None

	# text and kb
	if callback_data.decision == 'review':
		msg_id = "apply-check"
		kb_func = verification_request_ikb
	else:
		msg_id = "apply-checked"
		kb_func = verified_request_ikb

	async with async_session() as session:
		apply = await update_apply_status(session, callback_data.apply_id, status, cached_user.privileges_id)
		creator = apply.creator  # get in session

	await clb.answer()
	await clb.message.edit_text(
		l10n.format_value(msg_id, args={
			'status': status,
			'fullname': escape_md_v2(creator.full_name),
			'username': escape_md_v2(creator.telegram_username),
			'verified_by': escape_md_v2(verified_by)
		}),
		reply_markup=kb_func(l10n, apply.id)
	)
