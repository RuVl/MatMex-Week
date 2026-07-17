from aiogram.fsm.state import State, StatesGroup


class RegistrationsActions(StatesGroup):
	NAME_WAITING = State()
	CHECK_MEMBER = State()
	MANUAL_MEMBER_CHECK = State()
