from aiogram.fsm.state import StatesGroup, State

class States_purchases(StatesGroup):
    choose_category = State()
    choose_size = State()
    choose_product = State()
    confirm_purchase = State()
