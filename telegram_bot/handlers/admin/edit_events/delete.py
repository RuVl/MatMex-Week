from aiogram import Router, types
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import delete_event
from filters.main import LocalizedTextFilter
from keyboards.callback_factories import DeleteEventFactory
from keyboards.inline import events_ikb
from state_machines import EditEventsActions

delete_router = Router()


@delete_router.message(EditEventsActions.EDIT_EVENTS, LocalizedTextFilter("btn-delete-event"))
async def delete_event_btn_h(msg: types.Message, l10n: FluentLocalization):
	events = await events_ikb(l10n, True)
	await msg.answer(text=l10n.format_value("delete-events"), reply_markup=events)


@delete_router.callback_query(DeleteEventFactory.filter())
async def back_to_categories_h(callback: types.CallbackQuery, callback_data: DeleteEventFactory, l10n: FluentLocalization):
	async with async_session() as session:
		if callback_data.can_delete:
			await delete_event(session, callback_data.event_id)
	events = await events_ikb(l10n, callback_data.can_delete)
	await callback.bot.edit_message_text(
		text=l10n.format_value("delete-events"),
		reply_markup=events,
		chat_id=callback.message.chat.id,
		message_id=callback.message.message_id)
