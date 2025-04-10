from typing import Any, Callable

from aiogram import types
from fluent.runtime import FluentLocalization
from structlog import get_logger
from structlog.typing import FilteringBoundLogger

logger: FilteringBoundLogger = get_logger()


def get_user_context(user: types.User) -> dict:
	"""Creates a context dictionary with user information for logging."""
	context = {}
	if user:
		context.update({
			"user_id": user.id,
			"username": user.username,
			"full_name": f"{user.first_name} {user.last_name or ''}".strip(),
		})
	return context


def localized_text_filter(l10n_key: str) -> Callable[[str, dict[str, Any]], bool]:
	"""
	Creates a filter function that compares a text against a localized string.
	
	Args:
		l10n_key: The l10n key to be translated
		
	Returns:
		A filter function that takes a string and context dict with l10n
	"""

	def filter_function(text: str, context: dict[str, Any]) -> bool:
		l10n: FluentLocalization = context.get("l10n")
		if not l10n:
			return False
		localized_text = l10n.format_value(l10n_key)
		return text == localized_text

	return filter_function
