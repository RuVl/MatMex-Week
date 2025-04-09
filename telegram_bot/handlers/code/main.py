from aiogram import Router, types, F
from aiogram.enums import ParseMode
from fluent.runtime import FluentLocalization
from database import async_session

from database.methods import get_user_by_telegram_id

code_router = Router()


@code_router.message(F.text == 'Мой код')
async def code_button_pressed(msg: types.Message, l10n: FluentLocalization):
	telegram_id = msg.from_user.id
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, telegram_id)
		await msg.answer(
			l10n.format_value("code_message") + str(user.code),
			parse_mode=ParseMode.HTML
		)


