from aiogram.fsm.state import StatesGroup, State


class EditEventsActions(StatesGroup):
	EDIT_EVENTS = State()

	CREATE_EVENT = State()
	CHOOSE_EVENT_NAME = State()
	CHOOSE_EVENT_START_TIME = State()
	CHOOSE_EVENT_END_TIME = State()
	CHOOSE_EVENT_GRANTS = State()

