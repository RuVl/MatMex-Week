from aiogram import F
from aiogram import Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from keyboards import get_admin_keyboard, get_cancel_keyboard
from state_machines.states_accrual_of_points import AccrualOfPointsActions
from state_machines.states_admin import AdminActions

code_scanner_router = Router()
code_scanner_router.message.filter(
	F.text  # todo добавить чек на права из датабазы
)


@code_scanner_router.message(AdminActions.ADMIN_PANEL,
                             F.text == "Сканер кодов")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-event"), reply_markup=get_cancel_keyboard())
	await state.set_state(AccrualOfPointsActions.EVENT_WAITING)  # todo клавиатура мероприятий


@code_scanner_router.message(or_f(AccrualOfPointsActions.ID_WAITING, AccrualOfPointsActions.EVENT_WAITING),
                             F.text == "Отмена")
async def wrong_id(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("cancel-code-scanner-message"), reply_markup=get_admin_keyboard())
	await state.set_state(AdminActions.ADMIN_PANEL)


@code_scanner_router.message(AccrualOfPointsActions.EVENT_WAITING)  # todo фильтр доступа к меро
async def ask_for_id(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("ask-for-id"), reply_markup=get_cancel_keyboard())
	await state.set_state(AccrualOfPointsActions.ID_WAITING)


@code_scanner_router.message(AccrualOfPointsActions.EVENT_WAITING)
async def wrong_event_or_no_rights(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("wrong-event-or-no-rights"))
	await state.set_state(AccrualOfPointsActions.EVENT_WAITING)


@code_scanner_router.message(AccrualOfPointsActions.ID_WAITING)  # todo фильтр существоваия кода
async def give_points(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("give-points"), reply_markup=get_admin_keyboard())
	await state.set_state(AdminActions.ADMIN_PANEL)


@code_scanner_router.message(AccrualOfPointsActions.ID_WAITING)
async def wrong_id(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("wrong_id"))
	await state.set_state(AccrualOfPointsActions.ID_WAITING)
