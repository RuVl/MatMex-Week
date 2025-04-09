from os import environ
from typing import Final


class TelegramKeys:
	API_TOKEN: Final[str] = environ.get('TG_API_TOKEN')


class PostgresKeys:
	HOST: Final[str] = environ.get('DOCKER_POSTGRES_HOST', default='localhost')
	PORT: Final[str] = environ.get('DOCKER_POSTGRES_PORT', default='5432')

	USER: Final[str] = environ.get('POSTGRES_USER', default='postgres')
	PASSWORD: Final[str] = environ.get('POSTGRES_PASSWORD', default='')

	DATABASE: Final[str] = environ.get('POSTGRES_DB', default=USER)

	URL: Final[str] = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'


class RedisKeys:
	HOST: Final[str] = environ.get('DOCKER_REDIS_HOST', default='localhost')
	PORT: Final[str] = environ.get('DOCKER_REDIS_PORT', default='6379')

	DATABASE: Final[str] = environ.get('REDIS_DB', default='0')

	URL: Final[str] = f'redis://{HOST}:{PORT}/{DATABASE}'


class LoggerKeys:
	SHOW_DEBUG_LOGS: Final[bool] = environ.get('LOGGER_SHOW_DEBUG_LOGS', default=True)

	SHOW_DATETIME: Final[bool] = environ.get('LOGGER_SHOW_DATETIME', default=True)
	DATETIME_FORMAT: Final[str] = environ.get('LOGGER_DATETIME_FORMAT', default='%Y-%m-%d %H:%M:%S')
	TIME_IN_UTC: Final[bool] = environ.get('LOGGER_TIME_IN_UTC', default=True)

	RENDERER: Final[str] = environ.get('LOGGER_RENDERER', default='console')
	USE_COLORS_IN_CONSOLE: Final[bool] = environ.get('LOGGER_USE_COLORS_IN_CONSOLE', default=True)
