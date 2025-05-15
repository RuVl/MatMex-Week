from aiogram import Router, types
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from database import async_session
from database.enums import AdminPrivilege, ApplyStatus
from database.methods import update_apply_status, update_purchase_status
from database.models import User
from filters import FromBotToAdminFilter, IsSupportReplyFilter, PrivilegeFilter
from keyboards.callback_factories import PKApplyFactory, PurchaseApplyFactory, SupportFactory
from keyboards.inline import purchase_request_ikb, purchase_given_ikb, verification_request_ikb, verified_request_ikb
from utils import escape_md_v2
from .admin_menu import admin_menu_router

admin_router = Router()  # TODO Check privileges
admin_router.include_routers(admin_menu_router)


@admin_router.message(FromBotToAdminFilter(), IsSupportReplyFilter())
async def send_support_h(msg: types.Message, support_data: SupportFactory, l10n: FluentLocalization):
	try:
		await msg.bot.send_message(support_data.user_id, escape_md_v2(msg.text), reply_to_message_id=support_data.message_id)
	except:
		await msg.answer(l10n.format_value("support-sent-error"))
	else:
		await msg.answer(l10n.format_value("support-sent"))


@admin_router.callback_query(PKApplyFactory.filter(), PrivilegeFilter(AdminPrivilege.EDIT_PK_APPLY))
async def apply_verify_h(clb: CallbackQuery, callback_data: PKApplyFactory, l10n: FluentLocalization, cached_user: User):
	match callback_data.decision:
		case 'approve':
			status = ApplyStatus.APPROVED
			verified_by = cached_user.full_name
		case 'reject':
			status = ApplyStatus.REJECTED
			verified_by = cached_user.full_name
		case _:  # 'review' or any other case
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
		apply = await update_apply_status(
			session,
			callback_data.apply_id,
			status,
			cached_user.privileges_id
		)
		creator = apply.creator  # get in session

	await clb.answer()
	await clb.message.edit_text(
		l10n.format_value(msg_id, args={
			'status': status.value,
			'fullname': escape_md_v2(creator.full_name),
			'username': escape_md_v2(creator.telegram_username or 'None'),
			'verified_by': escape_md_v2(verified_by or '')
		}),
		reply_markup=kb_func(l10n, apply.id)
	)


@admin_router.callback_query(PurchaseApplyFactory.filter())
async def purchase_give_h(
	clb: CallbackQuery, callback_data: PurchaseApplyFactory, l10n: FluentLocalization, cached_user: User
):
	match callback_data.decision:
		case 'approve':
			status = ApplyStatus.APPROVED
			verified_by = cached_user.full_name
		case 'reject':
			status = ApplyStatus.REJECTED
			verified_by = cached_user.full_name
		case _:  # 'review' or any other case
			status = ApplyStatus.PENDING
			verified_by = None

	# text and kb
	if callback_data.decision == 'review':
		msg_id = "purchase-check"
		kb_func = purchase_request_ikb
	else:
		msg_id = "purchase-checked"
		kb_func = purchase_given_ikb

	async with async_session() as session:
		purchase = await update_purchase_status(
			session,
			callback_data.purchase_id,
			status,
		)
		customer = purchase.customer
		item = purchase.merch
	await clb.answer()
	await clb.message.edit_text(
		l10n.format_value(
			msg_id,
			args={
				'status': status.value,
				'fullname': escape_md_v2(customer.full_name),
				'itemname': escape_md_v2(item.full_name()),
				'username': escape_md_v2(customer.telegram_username or 'None'),
				'verified_by': escape_md_v2(verified_by or ''),
			},
		),
		reply_markup=kb_func(l10n, purchase.id),
	)
