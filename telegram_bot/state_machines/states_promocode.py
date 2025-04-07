from aiogram.fsm.state import StatesGroup, State


class PromocodeActions(StatesGroup):
	ENTER_PROMOCODE = State()
