from aiogram.fsm.state import StatesGroup, State

class ModerationActions(StatesGroup):
    ID_WAITING = State()
    RIGHTS_TYPE_INPUT = State()

