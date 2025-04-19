from aiogram import Router, types
from fluent.runtime import FluentLocalization

from keyboards.inline import events_ikb
from keyboards.callback_factories import DeleteEventFactory
from database.methods import delete_event
from database import async_session
from state_machines import EditEventsActions
from filters.main import LocalizedTextFilter

delete_router = Router()


@delete_router.message(EditEventsActions.EDIT_EVENTS, LocalizedTextFilter("btn-delete-event"))
async def handle_delete_event_btn(msg: types.Message, l10n: FluentLocalization):
	events = await events_ikb(l10n, True)
	await msg.answer(text=l10n.format_value("delete-events"), reply_markup=events)


@delete_router.callback_query(DeleteEventFactory.filter())
async def handle_back_to_categories(callback: types.CallbackQuery, l10n: FluentLocalization):
	data = DeleteEventFactory.unpack(callback.data)
	async with async_session() as session:
		if data.can_delete:
			await delete_event(session, data.event_id)
	events = await events_ikb(l10n, data.can_delete)
	await callback.bot.edit_message_text(
		text=l10n.format_value("delete-events"),
		reply_markup=events,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id)
