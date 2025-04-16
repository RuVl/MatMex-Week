from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from database import async_session
from database.methods import activate_promocode
from database.models import User
from filters import LocalizedTextFilter
from keyboards.common import menu_kb, cancel_kb
from state_machines import PromocodeActions
from utils import escape_md_v2

promocode_router = Router()


@promocode_router.message(LocalizedTextFilter("btn-enter-promocode"))
async def handle_promocode_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("promocode_enter"), reply_markup=cancel_kb(l10n))
	await state.set_state(PromocodeActions.ENTER_PROMOCODE)


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE, LocalizedTextFilter("btn-cancel"))
async def handle_promocode_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("cancel_message"), reply_markup=menu_kb(l10n))
	await state.clear()


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE)
async def handle_promocode_input(msg: types.Message, state: FSMContext, l10n: FluentLocalization, cached_user: User, log: FilteringBoundLogger):
	promocode_code = msg.text.strip()
	await log.adebug("log-promocode-entered", promocode=promocode_code)

	if cached_user is None:
		await log.awarning("user-not-found", telegram_id=msg.from_user.id)
		await msg.answer("Произошла ошибка: пользователь не найден", reply_markup=menu_kb(l10n))
		await state.clear()
		return

	async with async_session() as session:
		await session.refresh(cached_user)  # TODO это работать не будет 
		# Нужно переписать методы промокода, чтобы активация промокода возвращала активацию промокода или None.
		# Где None - промокод не активирован
		
		# Активируем промокод
		success, message, cost = await activate_promocode(session, promocode_code, cached_user.id)

		if success:
			await log.adebug("log-promocode-valid", cost=cost)
			# Используем новый баланс из базы данных
			await msg.answer(l10n.format_value("good-promo-message", args={
				'cost': cost,
				'balance': cached_user.balance
			}), reply_markup=menu_kb(l10n))
		else:
			await log.adebug("log-promocode-invalid", message=message)
			await msg.answer(l10n.format_value("sad-promo-message", args={
				'message': escape_md_v2(message)
			}), reply_markup=menu_kb(l10n))

	await state.clear()
