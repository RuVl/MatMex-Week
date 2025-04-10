from aiogram import Router, types, F
from aiogram.enums import ParseMode
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import get_user_by_telegram_id

profile_router = Router()


@profile_router.message(F.text == 'Профиль')
async def profile_button_pressed(message: types.Message, l10n: FluentLocalization):
	telegram_id = message.from_user.id
	async with async_session() as session:
		user = await get_user_by_telegram_id(session, telegram_id)

		full_name = user.full_name
		balance = user.balance
		await message.answer(
			l10n.format_value("Юзер:  " + full_name),
			ParseMode=ParseMode.HTML
		)
