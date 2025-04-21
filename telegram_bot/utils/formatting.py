"""
Utility functions for formatting data for display.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

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
	dt_tz = dt.replace(tzinfo=ZoneInfo("Europe/Moscow"))
	date_parts = []

	# Add weekday if needed
	if include_weekday:
		date_parts.append(f"{DAYS_RU[dt_tz.weekday()]}")

	# Add date with month in genitive case
	date_parts.append(f"{dt_tz.day} {MONTHS_RU_GENITIVE[dt_tz.month - 1]}")

	# Add time if needed
	if include_time:
		date_parts.append(f"{dt_tz.hour:02}:{dt_tz.minute:02}")

	return " ".join(date_parts)


def format_short_date(dt: datetime) -> str:
	"""Format date in short format DD.MM.YYYY"""
	dt_tz = dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Moscow"))
	return f"{dt_tz.day:02}.{dt_tz.month:02}.{dt_tz.year}"


def format_short_time(dt: datetime) -> str:
	"""Format time in short format HH:MM"""
	dt_tz = dt.replace(tzinfo=ZoneInfo("Europe/Moscow"))
	return f"{dt_tz.hour:02}:{dt_tz.minute:02}"


def format_event_datetime(dt: datetime) -> str:
	"""Format event datetime in standard format with weekday"""
	dt_tz = dt.replace(tzinfo=ZoneInfo("Europe/Moscow"))
	return f"{DAYS_RU[dt_tz.weekday()]} {dt_tz.day:02}.{dt_tz.month:02} {dt_tz.hour:02}:{dt_tz.minute:02}"


def format_event_datetime_with_year(dt: datetime) -> str:
	"""Format event datetime with year included"""
	dt_tz = dt.replace(tzinfo=ZoneInfo("Europe/Moscow"))
	return f"{DAYS_RU[dt_tz.weekday()]} {dt_tz.day:02}.{dt_tz.month:02}.{dt_tz.year} {dt_tz.hour:02}:{dt_tz.minute:02}"
