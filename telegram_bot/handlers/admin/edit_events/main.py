from aiogram import F, Router, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database.enums import AdminPrivilege
from filters.main import LocalizedTextFilter, PrivilegeFilter
from keyboards.common import admin_kb, edit_events_kb
from state_machines.admin import AdminActions
from state_machines.edit_events import EditEventsActions
from .create import create_router
from .delete import delete_router

edit_events_router = Router()
edit_events_router.include_routers(
	create_router,
	delete_router)
edit_events_router.message.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_EVENTS)
)
edit_events_router.callback_query.filter(
	PrivilegeFilter(AdminPrivilege.EDIT_EVENTS)
)


@edit_events_router.message(AdminActions.ADMIN_PANEL,
	LocalizedTextFilter("btn-edit-events"))
async def edit_events_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("edit-events-menu"), reply_markup=edit_events_kb(l10n))
	await state.set_state(EditEventsActions.EDIT_EVENTS)


@edit_events_router.callback_query(
	or_f(
		EditEventsActions.CHOOSE_EVENT_NAME,
		EditEventsActions.CHOOSE_EVENT_START_TIME,
		EditEventsActions.CHOOSE_EVENT_END_TIME,
	),
	F.data == "btn_cancel"
)
async def cancel_edit_event_h(callback: types.CallbackQuery, state: FSMContext, l10n: FluentLocalization):
	await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
	await callback.message.answer(l10n.format_value("cancel-edit-shop"), reply_markup=edit_events_kb(l10n))
	await state.set_state(EditEventsActions.EDIT_EVENTS)


@edit_events_router.message(EditEventsActions.EDIT_EVENTS, LocalizedTextFilter("btn-back"))
async def back_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("back-to-menu"), reply_markup=admin_kb(l10n))
	await state.set_state(AdminActions.ADMIN_PANEL)
