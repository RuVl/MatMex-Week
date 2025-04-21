"""
Utility functions for formatting data for display.
"""
from datetime import datetime

from .constants import DAYS_RU, MONTHS_RU_GENITIVE


def format_datetime(dt: datetime, include_weekday: bool = True, include_time: bool = True) -> str:
	"""
	Format datetime in a localized way.
	
	Args:
		dt: The datetime object to format
		include_weekday: Whether to include the weekday name
		include_time: Whether to include the time
		
	Returns:
		Formatted datetime string
	"""
	date_parts = []

	# Add weekday if needed
	if include_weekday:
		date_parts.append(f"{DAYS_RU[dt.weekday()]}")

	# Add date with month in genitive case
	date_parts.append(f"{dt.day} {MONTHS_RU_GENITIVE[dt.month - 1]}")

	# Add time if needed
	if include_time:
		date_parts.append(f"{dt.hour:02}:{dt.minute:02}")

	return " ".join(date_parts)


def format_short_date(dt: datetime) -> str:
	"""Format date in short format DD.MM.YYYY"""
	return f"{dt.day:02}.{dt.month:02}.{dt.year}"


def format_short_time(dt: datetime) -> str:
	"""Format time in short format HH:MM"""
	return f"{dt.hour:02}:{dt.minute:02}"


def format_event_datetime(dt: datetime) -> str:
	"""Format event datetime in standard format with weekday"""
	return f"{DAYS_RU[dt.weekday()]} {dt.day:02}.{dt.month:02} {dt.hour:02}:{dt.minute:02}"


def format_event_datetime_with_year(dt: datetime) -> str:
	"""Format event datetime with year included"""
	return f"{DAYS_RU[dt.weekday()]} {dt.day:02}.{dt.month:02}.{dt.year} {dt.hour:02}:{dt.minute:02}"
