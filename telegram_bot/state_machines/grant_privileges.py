from aiogram.fsm.state import State, StatesGroup


class GrantPrivilegesActions(StatesGroup):
	WAIT_NAME = State()
	CHOOSE_USER = State()
	PRIVILEGES_KB = State()
