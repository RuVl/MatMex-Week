import logging
from json import dumps

import structlog
from structlog import WriteLoggerFactory

from env import LoggerKeys


def get_structlog_config() -> dict:
	"""
	Get config for a structlog
	:return: dict with structlog config
	"""

	min_level = logging.DEBUG if LoggerKeys.SHOW_DEBUG_LOGS else logging.INFO

	return {
		"processors": get_processors(LoggerKeys),
		"cache_logger_on_first_use": True,
		"wrapper_class": structlog.make_filtering_bound_logger(min_level),
		"logger_factory": WriteLoggerFactory()
	}


def get_processors(log_config: LoggerKeys) -> list:
	"""
	Returns processors list for structlog
	:param log_config: LogConfig object with log parameters
	:return: processors list for structlog
	"""

	def custom_json_serializer(data, *args, **kwargs):
		"""
		JSON-objects custom serializer
		"""
		result = dict()

		if log_config.SHOW_DATETIME:
			result["timestamp"] = data.pop("timestamp")

		# Other two keys goes in this order
		for key in ("level", "event"):
			if key in data:
				result[key] = data.pop(key)

		# Remaining keys will be printed "as is" (usually in alphabet order)
		result.update(**data)
		return dumps(result, default=str)

	processors = [
		structlog.contextvars.merge_contextvars
	]

	# In some cases, there is no need to print a timestamp,
	# because it is already added by an upstream service, such as systemd
	if log_config.SHOW_DATETIME:
		processors.append(structlog.processors.TimeStamper(
			fmt=log_config.DATETIME_FORMAT,
			utc=log_config.TIME_IN_UTC
		))

	# Always add a log level
	processors.extend([
		structlog.processors.add_log_level,
		structlog.processors.StackInfoRenderer(),
		structlog.processors.format_exc_info,
	])

	match log_config.RENDERER:
		case 'json':
			processors.append(structlog.processors.JSONRenderer(serializer=custom_json_serializer))
		case 'console':
			processors.append(structlog.dev.ConsoleRenderer(colors=log_config.USE_COLORS_IN_CONSOLE, pad_level=True))

	return processors
