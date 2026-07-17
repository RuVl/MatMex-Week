"""
Utility functions for formatting data display using pendulum.
"""
import pendulum
from pendulum import set_locale

from env import TelegramKeys

# Set global locale
set_locale('ru')


def format_datetime(dt, include_weekday: bool = True, include_time: bool = True) -> str:
	"""
	Format datetime in a localized way.
	
	Args:
		dt: The datetime object to format
		include_weekday: Whether to include the weekday name
		include_time: Whether to include the time
		
	Returns:
		Formatted datetime string
	"""
	format_parts = []

	if include_weekday:
		format_parts.append('dddd')

	format_parts.append('D MMMM')

	if include_time:
		format_parts.append('HH:mm')

	dt = pendulum.instance(dt).in_tz(TelegramKeys.TZ)
	return dt.format(' '.join(format_parts))


def format_short_date(dt) -> str:
	"""Format date in short format DD.MM.YYYY"""
	dt = pendulum.instance(dt).in_tz(TelegramKeys.TZ)
	return dt.format('DD.MM.YYYY')


def format_short_time(dt) -> str:
	"""Format time in short format HH:MM"""
	dt = pendulum.instance(dt)
	return dt.in_tz(TelegramKeys.TZ).format('HH:mm')


def format_event_datetime(dt) -> str:
	"""Format event datetime in standard format with weekday"""
	dt = pendulum.instance(dt).in_tz(TelegramKeys.TZ)
	return f"{dt.format('dddd')} {dt.format('DD.MM')} {dt.format('HH:mm')}"


def format_event_datetime_with_year(dt) -> str:
	"""Format event datetime with year included"""
	dt = pendulum.instance(dt).in_tz(TelegramKeys.TZ)
	return f"{dt.format('dddd')} {dt.format('DD.MM.YYYY')} {dt.format('HH:mm')}"
