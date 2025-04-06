from aiogram.fsm.state import StatesGroup, State

class RegistrationsActions(StatesGroup):
    NAME_WAITING = State()
    CHECK_MEMBER = State()
