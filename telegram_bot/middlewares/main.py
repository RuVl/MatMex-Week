from aiogram import Dispatcher

from env import TelegramKeys
from includes import get_fluent_localization
from middlewares import L10nMw, DropEmptyCallbackMw, UserCacheMw, LoggingMw, ChatActionsMw


def register_middlewares(dp: Dispatcher):
	# Drop callback data with only space symbol
	dp.callback_query.outer_middleware(DropEmptyCallbackMw())

	# Localization
	locale = get_fluent_localization()
	l10n_mw = L10nMw(locale)
	dp.message.outer_middleware(l10n_mw)
	dp.callback_query.outer_middleware(l10n_mw)

	# Logging handlers (should be last)
	logging_mw = LoggingMw()
	dp.message.middleware(logging_mw)
	dp.callback_query.middleware(logging_mw)

	# Database user from cache or db
	user_cache_mw = UserCacheMw()
	dp.message.middleware(user_cache_mw)
	dp.callback_query.middleware(user_cache_mw)
	dp.shutdown.register(user_cache_mw.close)  # close storage connection

	# Typing by flag typing=True
	chat_actions_mw = ChatActionsMw(enabled=not TelegramKeys.WITHOUT_TYPING)
	dp.message.middleware(chat_actions_mw)
	dp.callback_query.middleware(chat_actions_mw)
