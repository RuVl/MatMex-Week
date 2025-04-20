from aiogram.fsm.state import State, StatesGroup


class AdminActions(StatesGroup):
	ADMIN_PANEL = State()
