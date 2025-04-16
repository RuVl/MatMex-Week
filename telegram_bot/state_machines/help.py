from aiogram.fsm.state import StatesGroup, State


class HelpActions(StatesGroup):
	MESSAGE_OR_CANCEL = State()
