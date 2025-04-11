from aiogram import Dispatcher

from includes import get_fluent_localization
from middlewares import L10nMiddleware, DropEmptyCallbackMiddleware
from middlewares.db_user import DBUserMiddleware
from middlewares.logging import LoggingMiddleware


def register_middlewares(dp: Dispatcher):
	# Drop callback data with only space symbol
	dp.callback_query.outer_middleware(DropEmptyCallbackMiddleware())

	# Localization
	locale = get_fluent_localization()
	l10n_middleware = L10nMiddleware(locale)
	dp.message.outer_middleware(l10n_middleware)
	dp.callback_query.outer_middleware(l10n_middleware)

	# Logging handlers
	logging_middleware = LoggingMiddleware()
	dp.message.middleware(logging_middleware)
	dp.message.middleware(logging_middleware)

	# Database user from cache or db
	db_user_middleware = DBUserMiddleware()
	dp.message.middleware(db_user_middleware)
	dp.shutdown.register(db_user_middleware.close)  # close storage connection
