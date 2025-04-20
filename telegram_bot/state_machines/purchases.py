from aiogram.fsm.state import State, StatesGroup


class PurchasesActions(StatesGroup):
	CHOOSE_CATEGORY = State()
	CHOOSE_SIZE = State()
	CHOOSE_ITEM = State()
	CONFIRM_PURCHASE = State()
