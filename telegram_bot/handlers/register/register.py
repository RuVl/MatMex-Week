from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from state_machines.states_registration import RegistrationsActions

register_router = Router()


# '/start'
@register_router.message(CommandStart())
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("hi"))
	await msg.answer(l10n.format_value("ask-name"))
	await msg.answer(l10n.format_value("talk-about-pc"))
	await state.set_state(RegistrationsActions.NAME_WAITING)
