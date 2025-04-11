from aiogram.fsm.state import StatesGroup, State


class AdminActions(StatesGroup):
	ADMIN_PANEL = State()
	SEND_SUPPORT = State()