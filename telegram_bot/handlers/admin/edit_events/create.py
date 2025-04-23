from zoneinfo import ZoneInfo

import dateparser
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import create_event, get_user_by_telegram_id
from env import TelegramKeys
from filters.main import LocalizedTextFilter
from keyboards.common import edit_events_kb
from keyboards.inline import cancel_ikb
from state_machines.edit_events import EditEventsActions

create_router = Router()


@create_router.message(EditEventsActions.EDIT_EVENTS, LocalizedTextFilter("btn-add-event"))
async def create_event_btn_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("event-creation"), reply_markup=types.ReplyKeyboardRemove())
	event_message = await msg.answer(l10n.format_value("ask-for-event-name"), reply_markup=cancel_ikb(l10n))

	await state.update_data(event_message_id=event_message.message_id)
	await state.set_state(EditEventsActions.CHOOSE_EVENT_NAME)


@create_router.message(EditEventsActions.CHOOSE_EVENT_NAME)
async def ask_for_event_name_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()
	state_data.update(event_name=msg.text.strip())

	await msg.delete()
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-event-visit-points"),
		reply_markup=cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("event_message_id")
	)

	await state.set_data(state_data)
	await state.set_state(EditEventsActions.CHOOSE_EVENT_VISIT_POINTS)


@create_router.message(EditEventsActions.CHOOSE_EVENT_VISIT_POINTS)
async def ask_for_event_name_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	if not msg.text.isdigit() or (visit_points := int(msg.text)) < 0:
		await msg.reply(l10n.format_value("event-creation"), reply_markup=cancel_ikb(l10n))
		return

	state_data = await state.get_data()
	state_data.update(visit_points=visit_points)

	await msg.delete()
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-event-start-time"),
		reply_markup=cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("event_message_id")
	)

	await state.set_data(state_data)
	await state.set_state(EditEventsActions.CHOOSE_EVENT_START_TIME)


@create_router.message(EditEventsActions.CHOOSE_EVENT_START_TIME)
async def ask_for_event_start_time_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()

	starts_at = msg.text.strip()
	if dateparser.parse(starts_at) is None:
		await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
		await msg.answer(l10n.format_value("wrong-datetime"))
		return

	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
	await msg.bot.edit_message_text(
		l10n.format_value("ask-for-event-end-time"),
		reply_markup=cancel_ikb(l10n),
		chat_id=msg.chat.id,
		message_id=state_data.get("event_message_id")
	)

	state_data.update(event_start_time=starts_at)
	await state.set_data(state_data)
	await state.set_state(EditEventsActions.CHOOSE_EVENT_END_TIME)


@create_router.message(EditEventsActions.CHOOSE_EVENT_END_TIME)
async def ask_for_event_end_time_h(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	state_data = await state.get_data()

	ends_at = dateparser.parse(msg.text.strip())
	if ends_at is None:
		await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
		await msg.answer(l10n.format_value("wrong-datetime"))
		return

	await state.set_data(state_data)

	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)
		starts_at = dateparser.parse(state_data.get("event_start_time", ''))
		if starts_at is not None:
			starts_at = starts_at.replace(tzinfo=ZoneInfo(TelegramKeys.TZ))

		await create_event(
			session=session,
			name=state_data.get("event_name", ''),
			visit_points=int(state_data.get("visit_points", 0)),
			creator_id=user.privileges_id,
			starts_at=starts_at,
			ends_at=ends_at.replace(tzinfo=ZoneInfo(TelegramKeys.TZ)),
		)

	await msg.delete()
	await msg.bot.delete_message(chat_id=msg.chat.id, message_id=state_data.get("event_message_id"))
	await msg.answer(l10n.format_value("event-created"), reply_markup=edit_events_kb(l10n))

	await state.clear()
	await state.set_state(EditEventsActions.EDIT_EVENTS)
