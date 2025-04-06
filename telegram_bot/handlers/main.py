from aiogram import Dispatcher, Router
from aiogram.types import Message

test_router = Router()


@test_router.message()
async def echo(msg: Message):
	await msg.reply(msg.text)


def register_handlers(dp: Dispatcher):
	# Register your handlers and routers here
	dp.include_router(test_router)
