from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from fluent.runtime import FluentLocalization

from config import MEDIA_DIR

schedule_router = Router()


@schedule_router.message(F.text == 'Расписание')
async def schedule_button_pressed(message: types.Message, l10n: FluentLocalization):
	text = l10n.format_value("week-title")

	image_from_pc = FSInputFile(MEDIA_DIR / "schedule.jpg")
	await message.answer_photo(
		image_from_pc,
		caption=text,
		parse_mode=ParseMode.HTML
	)
