from aiogram import Dispatcher, Router

from register import register_router


def register_all_handlers(dp: Dispatcher) -> None:
    main_router = Router()

    main_router.include_routers(register_router)
    
    dp.include_router(main_router)