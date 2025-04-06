from aiogram.fsm.state import StatesGroup, State

class States_moderation(StatesGroup):
    id_waiting = State()
    rights_type_input = State()

