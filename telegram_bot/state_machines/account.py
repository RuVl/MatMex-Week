from aiogram.fsm.state import State, StatesGroup


class AccountActions(StatesGroup):
	ACCOUNT_PANEL = State()
	NAME_WAITING = State()
