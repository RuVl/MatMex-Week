from .admin_menu import admin_menu_router
from .code_scanner import code_scanner_router
from .edit_events import edit_events_router
from .edit_shop import edit_shop_router
from .grant_event_privileges import grant_event_privileges_router
from .grant_privileges import grant_privileges_router
from .main import admin_router

__all__ = [
	"admin_router",
	"admin_menu_router",
	"edit_shop_router",
	"edit_events_router",
	"grant_privileges_router",
	"grant_event_privileges_router",
	"code_scanner_router"
]
