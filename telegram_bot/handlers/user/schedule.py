from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from database import async_session
from database.methods import get_event_by_id
from filters import LocalizedTextFilter
from keyboards.callback_factories import BackToEventsFactory, EventFactory
from keyboards.inline import event_actons_ikb, events_ikb
from utils import escape_md_v2, format_event_datetime

schedule_router = Router()


@schedule_router.message(LocalizedTextFilter("btn-schedule"))
async def schedule_button_h(msg: types.Message, l10n: FluentLocalization):
	image_from_pc = FSInputFile(MEDIA_DIR / "schedule.jpg")
	events = await events_ikb(l10n, False)
	await msg.answer_photo(photo=image_from_pc, caption=l10n.format_value("schedule-text-html"), parse_mode=ParseMode.HTML)
	await msg.answer(text=l10n.format_value("schedule-keyboard"), reply_markup=events)


@schedule_router.callback_query(BackToEventsFactory.filter())
async def back_to_categories_h(callback: types.CallbackQuery, callback_data: BackToEventsFactory, l10n: FluentLocalization):
	events = await events_ikb(l10n, callback_data.can_delete)
	await callback.bot.edit_message_text(
		text=l10n.format_value("schedule-keyboard"),
		reply_markup=events,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id)


@schedule_router.callback_query(EventFactory.filter())
async def in_event_h(callback: types.CallbackQuery, callback_data: EventFactory, l10n: FluentLocalization):
	async with async_session() as session:
		event = await get_event_by_id(session, callback_data.event_id)

	# Format dates using utility function
	starts_at_formatted = format_event_datetime(event.starts_at)
	ends_at_formatted = format_event_datetime(event.ends_at)

	await callback.bot.edit_message_text(
		text=l10n.format_value("event-value", args={
			'eventname': escape_md_v2(event.name),
			'startsat': escape_md_v2(starts_at_formatted),
			'endsat': escape_md_v2(ends_at_formatted),
			'eventgives': event.points if hasattr(event, 'points') else 50  # Use event points if available
		}),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
		reply_markup=event_actons_ikb(
			l10n,
			event_id=event.id,
			can_delete=callback_data.can_delete
		))
