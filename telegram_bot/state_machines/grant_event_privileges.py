from aiogram.fsm.state import State, StatesGroup


class GrantEventPrivilegesActions(StatesGroup):
	WAIT_NAME = State()
	CHOOSE_USER = State()
	PRIVILEGES_KB = State()
