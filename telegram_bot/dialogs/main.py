from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs


def register_dialogs(dp: Dispatcher):
	setup_dialogs(dp)