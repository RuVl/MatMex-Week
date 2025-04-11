from aiogram.fsm.state import StatesGroup, State


class AdminActions(StatesGroup):
	ADMIN_PANEL = State()