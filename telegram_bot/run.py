import asyncio

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from structlog.typing import FilteringBoundLogger

from env import TelegramKeys
from handlers import register_handlers
from includes import get_structlog_config, get_storage
from middlewares import register_middlewares


async def main():
	# Init logging
	structlog.configure(**get_structlog_config())

	# Init bot
	bot = Bot(
		token=TelegramKeys.API_TOKEN,
		default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
	)

	# Init dispatcher
	dp = Dispatcher(storage=get_storage())
	register_handlers(dp)
	register_middlewares(dp)

	# Start bot
	logger: FilteringBoundLogger = structlog.get_logger()
	await logger.ainfo("Starting the bot...")

	try:
		await dp.start_polling(
			bot,
			allowed_updates=dp.resolve_used_update_types()  # Get only registered updates
		)
	finally:
		await bot.session.close()
		await logger.ainfo("Bot stopped.")


# Start bot
asyncio.run(main())
