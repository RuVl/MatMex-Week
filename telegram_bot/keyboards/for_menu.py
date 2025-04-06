from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def create_keyboard():
    buttons_data = [
        ("Магазин", "shop"),
        ("Профиль", "profile"),
        ("Поддержка", "help"),
        ("Расписание", "schedule"),
        ("Мой код", "my_code"),
        ("Промокод", "promo_code")
    ]

    buttons = [
        KeyboardButton(text=text, callback_data=callback_data)
        for text, callback_data in buttons_data
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=[
        buttons[:3],
        buttons[3:],
    ])

    return keyboard
