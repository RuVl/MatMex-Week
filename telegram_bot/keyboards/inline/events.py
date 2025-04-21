from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import async_session
from database.methods import get_all_events
from keyboards.callback_factories import BackToEventsFactory, DeleteEventFactory, EventFactory


async def events_ikb(l10n, can_delete: bool) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	async with async_session() as session:
		events = await get_all_events(session)
	for event in events:
		builder.row(
			InlineKeyboardButton(text=event.name, callback_data=EventFactory(
				event_id=event.id,
				can_delete=can_delete,
			).pack()),
		)
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-event"))


def event_actions_ikb(l10n, can_delete: bool, event_id: int) -> InlineKeyboardMarkup:
	builder = InlineKeyboardBuilder()
	if can_delete:
		builder.row(InlineKeyboardButton(
			text=l10n.format_value("delete-this-event"),
			callback_data=DeleteEventFactory(
				event_id=event_id,
				can_delete=can_delete,
			).pack()),
		)
	builder.row(InlineKeyboardButton(
		text=l10n.format_value("btn-back"),
		callback_data=BackToEventsFactory(can_delete=can_delete).pack()))
	return builder.as_markup(resize_keyboard=True, input_field_placeholder=l10n.format_value("placeholder-get-back-to-item"))
