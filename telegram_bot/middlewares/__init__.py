L10N_FORMAT_KEY = "l10n"
LOGGING_KEY = "log"
USER_CACHE_KEY = "cached_user"

from .db_cache import UserCacheMw
from .drop_nothing import DropEmptyCallbackMw
from .localization import L10nMw
from .logging import LoggingMw
from .main import register_middlewares
from .spam_protection import SpamProtectionMw
