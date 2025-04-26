from aiogram import Dispatcher

from .admin import admin_router
from .user import user_router


def register_handlers(dp: Dispatcher):
	dp.include_routers(
		user_router,
		admin_router,
	)
