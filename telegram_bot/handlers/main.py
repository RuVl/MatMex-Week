from aiogram import Dispatcher, Router
from aiogram.types import Message
from .register import register_router
from .helping import help_router

def register_handlers(dp: Dispatcher):
	# Register your handlers and routers here
	dp.include_router(register_router)
	dp.include_router(help_router)
