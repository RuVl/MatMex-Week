from aiogram.fsm.state import StatesGroup, State

class AccrualOfPointsActions(StatesGroup):
    EVENT_WAITING = State()
    ID_WAITING = State()
