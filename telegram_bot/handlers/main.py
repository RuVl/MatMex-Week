from aiogram import Dispatcher, Router
from aiogram.types import Message
from .register import register_router
from .helping import help_router
from .code import code_router
from .promocode import promo_router
from .profile import profile_router
from .admin import main_admin_router

def register_handlers(dp: Dispatcher):
	# Register your handlers and routers here
	dp.include_router(register_router)
	dp.include_router(help_router)
	dp.include_router(code_router)
	dp.include_router(promo_router)
	dp.include_router(profile_router)
	dp.include_router(main_admin_router)