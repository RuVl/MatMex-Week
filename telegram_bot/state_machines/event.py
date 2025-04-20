from aiogram.fsm.state import State, StatesGroup


class EventActions(StatesGroup):
	ENTER_EVENT_PARAMS = State()
