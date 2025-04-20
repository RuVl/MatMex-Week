from aiogram.fsm.state import State, StatesGroup


class HelpActions(StatesGroup):
	MESSAGE_OR_CANCEL = State()
