# '/start'
from aiogram import Router, F, types
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from state_machines import States_registration
from fluent.runtime import FluentLocalization

register_router = Router()

@register_router.message(CommandStart())
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
    await msg.answer(l10n.format_value("hi"))
    await msg.answer(l10n.format_value("ask-name"))
    await msg.answer(l10n.format_value("talk_about_pc"))
    await state.set_state(States_registration.NAME_WAITING)