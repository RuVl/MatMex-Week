from aiogram.fsm.state import StatesGroup, State


class PurchasesActions(StatesGroup):
	CHOOSE_CATEGORY = State()
	CHOOSE_SIZE = State()
	CHOOSE_ITEM = State()
	CONFIRM_PURCHASE = State()
