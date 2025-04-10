import io
import uuid

import segno
from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization
from structlog.typing import FilteringBoundLogger

from config import MEDIA_DIR
from database import async_session
from database.methods import get_user_by_telegram_id
from filters import LocalizedTextFilter
from handlers.user.account import account_router
from handlers.user.help import support_router
from handlers.user.register import register_router
from handlers.user.shop import shop_router

user_router = Router()
user_router.include_routers(
	register_router,  # регистрация пользователя
	account_router,  # профиль пользователя
	support_router,  # поддержка пользователя
	shop_router  # отображение магазина у пользователя
)


@user_router.message(LocalizedTextFilter("btn-schedule"))
async def handle_schedule_button(msg: types.Message, l10n: FluentLocalization):
	text = l10n.format_value("week-title")

	image_from_pc = FSInputFile(MEDIA_DIR / "schedule.jpg")
	await msg.answer_photo(image_from_pc, caption=text, parse_mode=ParseMode.HTML)


STANDARD_SCALE = 10

@user_router.message(LocalizedTextFilter("btn-my-code"))
async def code_button_pressed(msg: types.Message, l10n: FluentLocalization, log: FilteringBoundLogger):
	telegram_id = msg.from_user.id
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, telegram_id)
		data = str(user.code)

		username_bot = (await msg.bot.me()).username
		message_type = "https://t.me/" + username_bot + "?start=" + data

		qrcode = segno.make(message_type, micro=False)

		buffer = io.BytesIO()
		qrcode.save(buffer, kind='png', scale=STANDARD_SCALE)

		buffer.seek(0)
		await msg.answer_photo(photo=types.BufferedInputFile(buffer.read(), "qrcode.png"), ParseMode=ParseMode.HTML)


@user_router.message(CommandStart(deep_link=True))
async def handle_start_deeplink(message: types.Message, command: CommandObject, l10n: FluentLocalization,
                                log: FilteringBoundLogger):
	payload = command.args
	await log.ainfo(payload)
	try:
		await log.ainfo("What is happened?")
		uuid.UUID(payload)
		await message.answer(
			l10n.format_value("deeplink-valid", {"uuid": payload})
			# todo начислить баллы
		)


	except ValueError:
		await message.answer(
			l10n.format_value("deeplink-invalid")
		)
