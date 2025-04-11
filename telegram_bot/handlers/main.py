from aiogram import Dispatcher

from .admin_menu import admin_router
from .promocode import promocode_router
from .user import user_router


def register_handlers(dp: Dispatcher):
	dp.include_routers(
		user_router,
		promocode_router,
		admin_router,
	)
