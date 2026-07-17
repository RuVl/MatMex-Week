from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import activate_promocode, get_user_activations, get_user_by_telegram_id
from database.models import User
from filters import LocalizedTextFilter
from keyboards.common import menu_kb, user_codes_kb
from state_machines import PromocodeActions
from utils import escape_md_v2

promocode_router = Router()


@promocode_router.message(LocalizedTextFilter("btn-enter-promocode"))
async def promocode_button_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("promocode-enter"), reply_markup=user_codes_kb(l10n))
	await state.set_state(PromocodeActions.ENTER_PROMOCODE)


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-cancel"))
async def promocode_cancel_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	kb = await menu_kb(l10n, msg.from_user.id)
	await msg.answer(l10n.format_value("cancel"), reply_markup=kb)
	await state.clear()


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-user-codes"))
async def promocode_list_h(msg: types.Message, l10n: FluentLocalization):
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		activations = await get_user_activations(session, user.id)

	if not activations:
		await msg.answer(l10n.format_value("no-promocodes"))
		return

	str_lst = '\n'.join(escape_md_v2(pa.promocode.code) for pa in activations)
	await msg.answer(str_lst)


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE)
async def promocode_input_h(msg: types.Message, cached_user: User, l10n: FluentLocalization):
	promocode_code = msg.text.strip()

	async with async_session() as session:
		success, error_code, cost = await activate_promocode(session, promocode_code, cached_user.id)

		if success:
			await msg.answer(l10n.format_value("promocode-activated", args={"cost": cost, "balance": cached_user.balance}))
		else:
			# Map error codes to localization keys
			error_mapping = {
				"not_found": "promocode-error-not-found",
				"deactivated": "promocode-error-deactivated",
				"expired": "promocode-error-expired",
				"max_uses_reached": "promocode-error-max-uses",
				"already_activated": "promocode-error-already-activated",
				"user_not_found": "promocode-error-user-not-found"
			}

			# Get a localized error message or use a default if the error code is unknown
			error_key = error_mapping.get(error_code, "promocode-error-unknown")
			await msg.answer(l10n.format_value(error_key))
