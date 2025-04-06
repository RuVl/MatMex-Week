# '/start'
from aiogram import Router, F, types
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from state_machines import States_registration
import l10n
register_router = Router()

@register_router.message(CommandStart())
async def start(msg: types.Message, state: FSMContext):
    await msg.answer(l10n.hi())
    await msg.answer(l10n.ask_name())
    await msg.answer(l10n.talk_about_pc())
    await state.set_state(States_registration.NAME_WAITING)