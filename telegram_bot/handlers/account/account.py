from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from keyboards import get_menu_keyboard, get_account_menu_keyboard, get_cancel_keyboard
from state_machines.states_account import AccountActions
from filters import FIO_filter

account_router = Router()
account_router.message.filter(
	F.text
)

@account_router.message(F.text == "Профиль")
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("account-temp"), reply_markup=get_account_menu_keyboard())
	await state.set_state(AccountActions.ACCOUNT_PANEL)

@account_router.message(AccountActions.ACCOUNT_PANEL,
						F.text == "Редактировать ФИО")
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("input-new-name"), reply_markup=get_cancel_keyboard())
	await state.set_state(AccountActions.NAME_WAITING)

@account_router.message(AccountActions.NAME_WAITING,
						F.text == "Отмена")
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("cancel-change-name"), reply_markup=get_account_menu_keyboard())
	await state.set_state(AccountActions.ACCOUNT_PANEL)
 
@account_router.message(AccountActions.NAME_WAITING,
                        FIO_filter())
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("name-changed")  + ", " + msg.text.strip() + "\\!", reply_markup=get_account_menu_keyboard())
	await state.set_state(AccountActions.ACCOUNT_PANEL)

@account_router.message(AccountActions.NAME_WAITING)
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("wrong-FIO"), reply_markup=get_cancel_keyboard())

@account_router.message(AccountActions.ACCOUNT_PANEL,
						F.text == "Я вообще-то в пк") #todo фильтр уже в пк
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("already-in-pc"), reply_markup=get_account_menu_keyboard())

@account_router.message(AccountActions.ACCOUNT_PANEL,
                           F.text == "В меню")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=get_menu_keyboard())
	await state.clear()
