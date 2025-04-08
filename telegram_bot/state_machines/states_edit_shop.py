from aiogram.fsm.state import StatesGroup, State

class EditShopActions(StatesGroup):
	EDIT_SHOP = State()

	CREATE_CATEGORY = State()

	EDIT_CATEGORY = State()
	IN_CATEGORY = State()

	CREATE_ITEM = State()
	DELETE_ITEM = State()

	SET_SIZE = State()
	SET_PRICE = State()
	SET_COUNT = State()
