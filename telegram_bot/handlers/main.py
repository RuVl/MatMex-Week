from aiogram import Dispatcher

from .admin import main_admin_router
from .code import code_router
from .helping import help_router
from .promocode import promo_router
from .register import register_router
from .schedule import schedule_router
from .account import account_router
from .shop import shop_router

def register_handlers(dp: Dispatcher):
	dp.include_routers(
		register_router,
		help_router,
		code_router,
		promo_router,
		account_router,
		schedule_router,
		main_admin_router,
		shop_router
	)
