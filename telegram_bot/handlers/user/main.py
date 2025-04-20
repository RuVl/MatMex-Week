import io
import uuid

import segno
from aiogram import Router, flags, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import FSInputFile
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR, QR_CODE_SCALE
from database import async_session
from database.enums import EventPrivilege
from database.methods import get_active_user_event_grants, get_user_by_code, get_user_by_telegram_id, give_point_for_event_by_user_id
from database.models import EventPrivilegeGrant, User
from filters import LocalizedTextFilter
from handlers.user.account import account_router
from handlers.user.help import support_router
from handlers.user.promocode import promocode_router
from handlers.user.register import register_router
from handlers.user.shop import shop_router

user_router = Router()
user_router.include_routers(
	register_router,  # регистрация пользователя
	account_router,  # профиль пользователя
	support_router,  # поддержка пользователя
	shop_router,  # отображение магазина у пользователя
	promocode_router
)


@user_router.message(LocalizedTextFilter("btn-schedule"))
@flags.chat_action()
async def show_schedule_h(msg: types.Message, l10n: FluentLocalization):
	image_from_pc = FSInputFile(MEDIA_DIR / "schedule.jpg")
	await msg.answer_photo(photo=image_from_pc, caption=l10n.format_value("schedule-text-html"), parse_mode=ParseMode.HTML)


@user_router.message(LocalizedTextFilter("btn-my-code"))
async def show_my_qr_h(msg: types.Message):
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, msg.from_user.id)

	# Create the link and qr-code
	link = await create_start_link(bot=msg.bot, payload=str(user.code), encode=True)
	qrcode = segno.make(link, micro=False)

	# Save qr-code to buffer
	buffer = io.BytesIO()
	qrcode.save(buffer, kind='png', scale=QR_CODE_SCALE)
	buffer.seek(0)

	await msg.answer_photo(photo=types.BufferedInputFile(buffer.read(), "qrcode.png"))


@user_router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def give_event_points_h(msg: types.Message, command: CommandObject, cached_user: User, l10n: FluentLocalization):
	async with async_session() as session:
		# Получаем пользователя, которому начислить баллы
		user = await get_user_by_code(session, uuid.UUID(command.args))
		if user is None:
			await msg.answer(l10n.format_value("deeplink-invalid"))
			return

		# получить привилегии на ивент пользователя
		event_grants = await get_active_user_event_grants(session, cached_user.id)
		event_grants: list[EventPrivilegeGrant] = filter(
			lambda eg: eg.privileges & EventPrivilege.CAN_GIVE_POINTS, event_grants)

		if not event_grants:
			await msg.answer(l10n.format_value("no-rights"))

		# TODO кнопка с вопросом на какое мероприятие начислять, если их > 1
		# Пока что начислим сразу на все мероприятия
		for event_grant in event_grants:
			success = await give_point_for_event_by_user_id(session, user.id, event_grant.event_id)

			if success:
				await msg.answer(l10n.format_value("points-awarded"))
				await msg.bot.send_message(user.telegram_id, l10n.format_value("points-awarded"))
			else:
				await msg.answer(l10n.format_value("already-received"))
