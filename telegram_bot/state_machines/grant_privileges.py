from aiogram.fsm.state import StatesGroup, State


class GrantPrivilegesActions(StatesGroup):
	WAIT_NAME = State()
	CHOOSE_USER = State()
	PRIVILEGES_KB = State()
