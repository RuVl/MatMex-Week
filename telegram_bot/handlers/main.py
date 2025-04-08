from aiogram import Dispatcher

from .admin import main_admin_router
from .code import code_router
from .helping import help_router
from .profile import profile_router
from .promocode import promo_router
from .register import register_router
from .schedule import schedule_router
from .shop import shop_router


def register_handlers(dp: Dispatcher):
	# Register your handlers and routers here
	dp.include_router(register_router)
	dp.include_router(help_router)
	dp.include_router(code_router)
	dp.include_router(promo_router)
	dp.include_router(profile_router)
	dp.include_router(schedule_router)
	dp.include_router(main_admin_router)
	dp.include_router(shop_router)
