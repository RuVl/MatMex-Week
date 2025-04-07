from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from aiogram import F

from keyboards import get_admin_keyboard, get_menu_keyboard
from state_machines.states_admin import AdminActions
from .code_scanner import code_scanner_router
from .edit_shop import edit_shop_router
main_admin_router = Router()
main_admin_router.message.filter(
	F.text #todo добавить чек на права из датабазы
)
main_admin_router.include_router(code_scanner_router)
main_admin_router.include_router(edit_shop_router)

@main_admin_router.message(F.text == "Админ панель")
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("hello-admin"), reply_markup=get_admin_keyboard())
	await state.set_state(AdminActions.ADMIN_PANEL)

@main_admin_router.message(AdminActions.ADMIN_PANEL, 
                           F.text == "В меню")
async def ask_for_event(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=get_menu_keyboard())
	await state.clear()
