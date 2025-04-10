from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR
from database import async_session
from database.methods import get_user_by_telegram_id
from handlers.user.account import account_router
from handlers.user.help import support_router
from handlers.user.register import register_router
from handlers.user.shop import shop_router
from handlers.utils import localized_text_filter, logger, get_user_context

user_router = Router()
user_router.include_routers(
	register_router,  # регистрация пользователя
	account_router,  # профиль пользователя
	support_router,  # поддержка пользователя
	shop_router  # отображение магазина у пользователя
)


@user_router.message(F.text.func(localized_text_filter("btn-schedule")))
async def handle_schedule_button(msg: types.Message, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_schedule_button")

	text = l10n.format_value("week-title")

	image_from_pc = FSInputFile(MEDIA_DIR / "schedule.jpg")
	await msg.answer_photo(image_from_pc, caption=text, parse_mode=ParseMode.HTML)

	log.info("log-handler-completed")


@user_router.message(F.text.func(localized_text_filter("btn-my-code")))
async def handle_my_code_button(msg: types.Message, l10n: FluentLocalization):
	log = logger.bind(**get_user_context(msg.from_user))
	log.info("log-handler-called", handler="handle_my_code_button")

	telegram_id = msg.from_user.id
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, telegram_id)
		await msg.answer(l10n.format_value("code_message") + str(user.code), parse_mode=ParseMode.HTML)

	log.info("log-handler-completed")
