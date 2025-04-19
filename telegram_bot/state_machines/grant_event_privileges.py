from aiogram.fsm.state import StatesGroup, State


class GrantEventPrivilegesActions(StatesGroup):
	WAIT_NAME = State()
	CHOOSE_USER = State()
	PRIVILEGES_KB = State()
