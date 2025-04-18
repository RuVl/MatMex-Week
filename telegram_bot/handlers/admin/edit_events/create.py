from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger
from datetime import datetime

from keyboards.common import edit_events_kb
from keyboards.inline import cancel_ikb
from state_machines.edit_events import EditEventsActions
from filters.main import LocalizedTextFilter
from database.methods import create_event, get_user_by_telegram_id
from database import async_session

edit_events_create_router = Router()


@edit_events_create_router.message(EditEventsActions.EDIT_EVENTS, LocalizedTextFilter("btn-add-event"))
async def handle_create_event_btn(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_create_event_btn")
	await msg.answer(l10n.format_value("event-creation"), reply_markup=types.ReplyKeyboardRemove())
	event_message = await msg.answer(l10n.format_value("ask-for-event-name"), reply_markup=cancel_ikb(l10n))
	await state.update_data(event_message_id=event_message.message_id)
	await state.set_state(EditEventsActions.CHOOSE_EVENT_NAME)
	await log.adebug("log-state-changed", state=EditEventsActions.CHOOSE_EVENT_NAME.state)


@edit_events_create_router.message(EditEventsActions.CHOOSE_EVENT_NAME, F.text)
async def handle_ask_for_event_name(msg: types.Message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_event_name")

	state_data = await state.get_data()
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-event-start-time"),
		reply_markup=cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("event_message_id"))
	await state.set_state(EditEventsActions.CHOOSE_EVENT_START_TIME)
	await state.update_data(event_name=msg.text)
	await log.adebug("log-state-changed", state=EditEventsActions.CHOOSE_EVENT_START_TIME.state)


@edit_events_create_router.message(EditEventsActions.CHOOSE_EVENT_START_TIME)
async def handle_ask_for_event_start_time(msg: types.message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_event_start_time")
	state_data = await state.get_data()
	try:
		datetime.strptime(msg.text.strip(), "%d.%m.%Y %H:%M")
	except ValueError:
		await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
		await msg.answer(l10n.format_value("wrong-datetime"))
		return

	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-event-end-time"),
		reply_markup=cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("event_message_id"))
	await state.update_data(event_start_time=msg.text.strip())
	await state.set_state(EditEventsActions.CHOOSE_EVENT_END_TIME)
	await log.adebug("log-state-changed", state=EditEventsActions.CHOOSE_EVENT_END_TIME.state)


@edit_events_create_router.message(EditEventsActions.CHOOSE_EVENT_END_TIME)
async def handle_ask_for_event_end_time(msg: types.message, state: FSMContext, l10n: FluentLocalization, log: FilteringBoundLogger):
	await log.adebug("log-admin-action", action="handle_ask_for_event_end_time")
	try:
		datetime.strptime(msg.text.strip(), "%d.%m.%Y %H:%M")
	except ValueError:
		await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
		await msg.answer(l10n.format_value("wrong-datetime"))
		return

	await state.update_data(event_end_time=msg.text.strip())
	state_data = await state.get_data()

	async with async_session() as session:
		creator = await get_user_by_telegram_id(session, msg.from_user.id)
		await create_event(
			session=session,
			name=state_data.get("event_name"),
			creator_id=creator.id,
			starts_at=datetime.strptime(state_data.get(
				"event_start_time"), "%d.%m.%Y %H:%M"),
			ends_at=datetime.strptime(state_data.get(
				"event_end_time"), "%d.%m.%Y %H:%M"),
		)

	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=state_data.get("event_message_id"))
	await msg.answer(l10n.format_value("event-created"), reply_markup=edit_events_kb(l10n))
	await state.clear()
	await state.set_state(EditEventsActions.EDIT_EVENTS)
	await log.adebug("log-state-changed", state=EditEventsActions.EDIT_EVENTS.state)
