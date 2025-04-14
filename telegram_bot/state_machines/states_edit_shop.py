from aiogram.fsm.state import StatesGroup, State

class EditShopActions(StatesGroup):
	EDIT_SHOP = State()

	CREATE_CATEGORY = State()
	DELETE_CATEGORY = State()
	EDIT_CATEGORY = State()
	IN_CATEGORY = State()

	CREATE_ITEM = State()
	CHOOSE_ITEM_NAME = State()
	CHOOSE_ITEM_IMAGE = State()
	CHOOSE_ITEM_SIZE = State()
	CHOOSE_ITEM_FULL_PRICE = State()
	CHOOSE_ITEM_DISCOUNT_PRICE = State()
	CHOOSE_ITEM_AVAILABLE_COUNT = State()
	CHOOSE_ITEM_IN_STOCK = State()

	DELETE_ITEM = State()
	DELETE_ITEM_CHOOSE_CATEGORY = State()