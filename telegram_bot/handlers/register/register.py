from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization
from aiogram.enums import ParseMode
from aiogram import F

from state_machines.states_registration import RegistrationsActions
from filters import FIO_filter
from keyboards import yes_no_kb

register_router = Router()
register_router.message.filter(
    F.text
)

# '/start'
@register_router.message(CommandStart())
async def start(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("hi"))
	await msg.answer(l10n.format_value("ask-name"))
	await msg.answer(l10n.format_value("talk-about-pc"))
	await state.set_state(RegistrationsActions.NAME_WAITING)

@register_router.message(RegistrationsActions.NAME_WAITING,
                                FIO_filter())
async def input_FIO(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
	await msg.answer(l10n.format_value("thanks-FIO") +", " + msg.text.strip() +"\!")
	await msg.answer(l10n.format_value("ask-pc"), reply_markup=yes_no_kb())
	await state.set_state(RegistrationsActions.CHECK_MEMBER)

@register_router.message(RegistrationsActions.NAME_WAITING)
async def wrong_FIO_format(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
    await msg.answer(l10n.format_value("wrong-FIO"))
    await state.set_state(RegistrationsActions.NAME_WAITING)
    

@register_router.message(RegistrationsActions.CHECK_MEMBER,
                         F.text == 'Да')
async def in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
    await msg.answer("Круто")
 
@register_router.message(RegistrationsActions.CHECK_MEMBER,
                               F.text == 'Нет')
async def not_in_pc(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
    await msg.answer("Не круто")