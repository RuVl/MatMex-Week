import io

import segno
from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import get_user_by_telegram_id, update_user_balance

code_router = Router()

STANDARD_SCALE = 10


@code_router.message(F.text == 'Мой код')
async def code_button_pressed(msg: types.Message, l10n: FluentLocalization):
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


@code_router.message(CommandStart(deep_link=True))
async def handle_start_deeplink(message: types.Message, command: CommandObject):
    # command.args будет содержать payload
    payload = command.args

    await message.answer(
        f"Привет! Вы перешли по ссылке с данными юзера: `{payload}`.\n"
        f"Теперь я могу использовать эти данные для начисления ему баллов!"
    )

    update_user_balance()  # todo подумать над тем как реализовать это начисление
