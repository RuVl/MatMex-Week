from aiogram.fsm.state import State, StatesGroup


class AccrualOfPointsActions(StatesGroup):
	EVENT_WAITING = State()
	ID_WAITING = State()
