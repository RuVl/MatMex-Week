from aiogram.fsm.state import StatesGroup, State


class AccountActions(StatesGroup):
	ACCOUNT_PANEL = State()
	NAME_WAITING = State()