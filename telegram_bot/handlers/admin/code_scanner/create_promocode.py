import io
import segno

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.enums import AdminPrivilege
from database.methods import create_promocode, get_promocode_by_code, get_user_by_telegram_id
from filters import AdminPromocodeCreatingFilter, LocalizedTextFilter, PrivilegeFilter
from keyboards.common import admin_kb, cancel_kb, yes_no_kb
from state_machines import AdminActions, AdminPromocodeActions
from utils import escape_md_v2
from config import QR_CODE_SCALE

code_scanner_router = Router()
code_scanner_router.message.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_PROMOCODES)
)
code_scanner_router.callback_query.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_PROMOCODES)
)


@code_scanner_router.message(LocalizedTextFilter("btn-create-promo"))
async def create_promocode_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-promo-for-creating"), reply_markup=cancel_kb(l10n))
	await state.set_state(AdminPromocodeActions.ENTER_PROMOCODE)


@code_scanner_router.message(AdminPromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-yes"))
async def confirm_promocode_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-cost-promocode"), reply_markup=types.ReplyKeyboardRemove())
	await state.set_state(AdminPromocodeActions.ASK_FOR_COST)


@code_scanner_router.message(AdminPromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-no"))
async def reject_promocode_h(msg: types.Message, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-promo-for-creating"), reply_markup=cancel_kb(l10n))


@code_scanner_router.message(AdminPromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-cancel"))
async def back_to_menu_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)


@code_scanner_router.message(AdminPromocodeActions.ASK_FOR_COST)
async def promocode_cost_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	if not await AdminPromocodeCreatingFilter().__call__(msg):
		await msg.answer(l10n.format_value("wrong-cost"))
		return

	cost = int(msg.text)
	await state.update_data(cost_of_code=cost)

	await msg.answer(l10n.format_value("ask-for-max-uses"))
	await state.set_state(AdminPromocodeActions.ASK_FOR_MAX_USAGES)


@code_scanner_router.message(AdminPromocodeActions.ASK_FOR_MAX_USAGES)
async def promocode_max_usages_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	if not await AdminPromocodeCreatingFilter().__call__(msg):
		await msg.answer(l10n.format_value("wrong-usages"))
		return

	max_usages = int(msg.text)
	state_data = await state.get_data()
	promo_code = state_data.get("name_of_code")
	promo_cost = state_data.get("cost_of_code")

	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)

		if user.privileges_id is None:
			await msg.answer(l10n.format_value("you-have-not-rights"))
			return

		try:
			promocode = await create_promocode(
				session,
				promo_code,
				promo_cost,
				user.privileges_id,
				max_usages,
				None
			)
			# Create the link and qr-code
			link = await create_start_link(bot=msg.bot, payload=str(promocode.code), encode=True)
			qrcode = segno.make(link, micro=False)

			# Save qr-code to buffer
			buffer = io.BytesIO()
			qrcode.save(buffer, kind='png', scale=QR_CODE_SCALE)
			buffer.seek(0)

			await msg.answer_photo(
							photo=types.BufferedInputFile(buffer.read(), "qrcode.png"),
							caption=l10n.format_value("show-this-qr")
            )
   
			await log.adebug("promocode-created", code=promo_code, cost=promo_cost, max_uses=max_usages, creator_id=user.id)

			await msg.answer(
				l10n.format_value("promo-added", args={
					"code": escape_md_v2(promo_code),
					"cost": promo_cost,
					"max_uses": max_usages
				}),
				reply_markup=admin_kb(l10n)
			)

			await state.set_state(AdminActions.ADMIN_PANEL)
		except Exception as e:
			await log.aerror("promocode-creation-failed", error=str(e), code=promo_code)
			await msg.answer(l10n.format_value("promocode-creation-error"))


@code_scanner_router.message(AdminPromocodeActions.ENTER_PROMOCODE)
async def promocode_code_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	promo_code = msg.text.strip()

	# Validate promocode format
	if not promo_code or len(promo_code) < 5:
		await msg.answer(l10n.format_value("promocode-too-short"))
		return

	if len(promo_code) > 25:
		await msg.answer(l10n.format_value("promocode-too-long"))
		return

	async with async_session() as session:
		existing_code = await get_promocode_by_code(session, promo_code)

		if existing_code is not None:
			await msg.answer(l10n.format_value("promo_exist"))
			return

	await log.adebug("promocode-creation-started", code=promo_code)
	await state.update_data(name_of_code=promo_code)
	await msg.answer(l10n.format_value("ask-for-attend-promocode"), reply_markup=yes_no_kb(l10n))
