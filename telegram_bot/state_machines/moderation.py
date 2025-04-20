from aiogram.fsm.state import State, StatesGroup


class ModerationActions(StatesGroup):
	ID_WAITING = State()
	RIGHTS_TYPE_INPUT = State()
