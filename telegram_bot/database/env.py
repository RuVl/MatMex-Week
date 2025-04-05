from os import environ
from pathlib import Path
from typing import Final


class PostgresKeys:
    HOST: Final[str] = environ.get('DOCKER_POSTGRES_HOST', default='postgres')
    PORT: Final[str] = environ.get('DOCKER_POSTGRES_PORT', default='5432')

    USER: Final[str] = environ.get('POSTGRES_USER', default='postgres')
    PASSWORD: Final[str] = environ.get('POSTGRES_PASSWORD', default='')

    DATABASE: Final[str] = environ.get('POSTGRES_DB', default=USER)

    URL: Final[str] = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'