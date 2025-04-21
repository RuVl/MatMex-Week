from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, InputMediaPhoto
from fluent.runtime import FluentLocalization
from zoneinfo import ZoneInfo

from config import MEDIA_DIR
from filters import LocalizedTextFilter
from keyboards.inline import events_ikb, event_actons_ikb
from keyboards.callback_factories import EventFactory, BackToEventsFactory
from utils import escape_md_v2

from database import async_session
from database.methods import get_event_by_id

schedule_router = Router()


@schedule_router.message(LocalizedTextFilter("btn-schedule"))
async def handle_schedule_button(msg: types.Message, l10n: FluentLocalization):
	image_from_pc = FSInputFile(MEDIA_DIR / "schedule.jpg")
	events = await events_ikb(l10n, False)
	await msg.answer_photo(
            photo=image_from_pc,
            caption=l10n.format_value("schedule-text-html"),
            parse_mode=ParseMode.HTML,)
	await msg.answer(text=l10n.format_value("schedule-keyboard"), reply_markup=events)


@schedule_router.callback_query(BackToEventsFactory.filter())
async def handle_back_to_categories(callback: types.CallbackQuery, callback_data: BackToEventsFactory, l10n: FluentLocalization):
	events = await events_ikb(l10n, callback_data.can_delete)
	await callback.bot.edit_message_text(
		text=l10n.format_value("schedule-keyboard"),
		reply_markup=events,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id)


DAYS_RU = ['Понедельник', 'Вторник', 'Среда',
           'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


@schedule_router.callback_query(EventFactory.filter())
async def handle_in_event(callback: types.CallbackQuery, callback_data: EventFactory, l10n: FluentLocalization):
	async with async_session() as session:
		event = await get_event_by_id(session, callback_data.event_id)
	starts_at = event.starts_at.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Moscow"))
	ends_at = event.ends_at.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Moscow"))
	await callback.bot.edit_message_text(
		text=l10n.format_value("event-value",  args={
			'eventname': escape_md_v2(event.name),
			'startsat': escape_md_v2(f"{DAYS_RU[starts_at.weekday()]} {starts_at.day:02}.{starts_at.month:02} {starts_at.hour:02}:{starts_at.minute:02}"),
			'endsat': escape_md_v2(f"{DAYS_RU[ends_at.weekday()]} {ends_at.day:02}.{ends_at.month:02} {ends_at.hour:02}:{ends_at.minute:02}"),
			'eventgives': 50
		}),
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id,
		reply_markup=event_actons_ikb(l10n, event_id=event.id, can_delete=callback_data.can_delete))
