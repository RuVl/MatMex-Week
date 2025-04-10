from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from fluent.runtime import FluentLocalization

from database import async_session
from database.methods import activate_promocode, get_user_by_telegram_id
from handlers.utils import logger, get_user_context, localized_text_filter
from keyboards.common import get_menu_kb, get_cancel_kb
from state_machines.states_promocode import PromocodeActions

promocode_router = Router()


@promocode_router.message(F.text.func(localized_text_filter("btn-enter-promocode")))
async def handle_promocode_button(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
    log = logger.bind(**get_user_context(msg.from_user))
    log.info("log-handler-called", handler="handle_promocode_button")

    await msg.answer(
        l10n.format_value("promocode_enter"),
        reply_markup=get_cancel_kb(l10n)
    )
    await state.set_state(PromocodeActions.ENTER_PROMOCODE)

    log.info("log-state-changed", state=PromocodeActions.ENTER_PROMOCODE.state)
    log.info("log-handler-completed")


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE, F.text.func(localized_text_filter("btn-cancel")))
async def handle_promocode_cancel(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
    log = logger.bind(**get_user_context(msg.from_user))
    log.info("log-handler-called", handler="handle_promocode_cancel")

    await msg.answer(l10n.format_value("cancel_message"),
                     reply_markup=get_menu_kb(l10n))
    await state.clear()

    log.info("log-state-changed", state="cleared")
    log.info("log-handler-completed")


@promocode_router.message(PromocodeActions.ENTER_PROMOCODE)
async def handle_promocode_input(msg: types.Message, state: FSMContext, l10n: FluentLocalization):
    log = logger.bind(**get_user_context(msg.from_user))
    log.info("log-handler-called", handler="handle_promocode_input")
    log.info("log-promocode-entered", promocode=msg.text)

    promocode_code = msg.text.strip()

    async with async_session() as session:
        # Получаем пользователя
        user = await get_user_by_telegram_id(session, msg.from_user.id)
        if not user:
            log.error("user-not-found", telegram_id=msg.from_user.id)
            await msg.answer("Произошла ошибка: пользователь не найден", reply_markup=get_menu_kb(l10n))
            await state.clear()
            return

        # Активируем промокод
        success, message, cost = await activate_promocode(session, promocode_code, user.id)

        if success:
            log.info("log-promocode-valid", cost=cost)
            # Используем новый баланс из базы данных
            balance_text = f"\nВаш баланс: {user.balance} баллов"
            await msg.answer(l10n.format_value("good-promo-message") + f" ({cost} баллов)" + balance_text,
                             reply_markup=get_menu_kb(l10n))
        else:
            log.info("log-promocode-invalid", message=message)
            await msg.answer(l10n.format_value("sad-promo-message") + f"\n{message}",
                             reply_markup=get_menu_kb(l10n))

    await state.clear()
    log.info("log-state-changed", state="cleared")
    log.info("log-handler-completed")
