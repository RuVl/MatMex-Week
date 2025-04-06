from aiogram import Dispatcher, Router
from aiogram.types import Message
from .register import register_router

def register_handlers(dp: Dispatcher):
	# Register your handlers and routers here
	dp.include_router(register_router)
