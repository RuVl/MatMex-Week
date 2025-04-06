from aiogram import Dispatcher

from includes.fluent import get_fluent_localization
from middlewares import L10nMiddleware, DropEmptyCallbackMiddleware


def register_middlewares(dp: Dispatcher):
	# Register your middlewares here
	locale = get_fluent_localization()

	dp.callback_query.outer_middleware(DropEmptyCallbackMiddleware())

	dp.message.outer_middleware(L10nMiddleware(locale))
	dp.callback_query.outer_middleware(L10nMiddleware(locale))
