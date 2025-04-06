from aiogram import Dispatcher

from fluent import get_fluent_localization
from middlewares.drop_nothing import DropEmptyCallbackMiddleware
from middlewares.localization import L10nMiddleware


def register_middlewares(dp: Dispatcher):
    # Init fluent
    locale = get_fluent_localization()

    dp.callback_query.outer_middleware(DropEmptyCallbackMiddleware())

    dp.message.outer_middleware(L10nMiddleware(locale))
    dp.callback_query.outer_middleware(L10nMiddleware(locale))