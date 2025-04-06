from aiogram.fsm.state import StatesGroup, State

class States_registration(StatesGroup):
    name_waiting = State()
    check_member = State()
