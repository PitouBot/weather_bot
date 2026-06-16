from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🌤️ Погода сейчас", callback_data="weather"),
        InlineKeyboardButton(text="🌍 Мой город", callback_data="my_city")
    ],
    [
        InlineKeyboardButton(text="📌 Установить город", callback_data="set_city"),
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    ]
])

