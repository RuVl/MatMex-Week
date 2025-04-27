from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware

from includes import get_fluent_localization
from middlewares import DropEmptyCallbackMw, L10N_FORMAT_KEY, L10nMw, LOGGING_KEY, LoggingMw, USER_CACHE_KEY, UserCacheMw
from middlewares.single_message import SingleMessageMw


def register_middlewares(dp: Dispatcher):
	# Single message (in-memory locking)
	dp.message.outer_middleware(SingleMessageMw())

	# Drop callback data with only space symbol
	dp.callback_query.outer_middleware(DropEmptyCallbackMw())

	# Localization
	locale = get_fluent_localization()
	l10n_mw = L10nMw(locale, L10N_FORMAT_KEY)
	dp.message.outer_middleware(l10n_mw)
	dp.callback_query.outer_middleware(l10n_mw)

	# Spam protection
	# spam_protection_mw = SpamProtectionMw()
	# dp.message.outer_middleware(spam_protection_mw)
	# dp.callback_query.outer_middleware(spam_protection_mw)
	# dp.shutdown.register(spam_protection_mw.close)

	# Logging handlers (should be last)
	logging_mw = LoggingMw(LOGGING_KEY)
	dp.message.middleware(logging_mw)
	dp.callback_query.middleware(logging_mw)

	# Database user from cache or db
	user_cache_mw = UserCacheMw(USER_CACHE_KEY)
	dp.message.middleware(user_cache_mw)
	dp.callback_query.middleware(user_cache_mw)
	dp.shutdown.register(user_cache_mw.close)  # close storage connection

	# Typing
	dp.message.middleware(ChatActionMiddleware())
