from aiogram.fsm.state import State, StatesGroup


class PromocodeActions(StatesGroup):
	ENTER_PROMOCODE = State()
	ASK_FOR_COST = State()
	ASK_FOR_MAX_USAGES = State()
