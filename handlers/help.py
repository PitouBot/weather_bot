import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📋 *Полный список команд:*\n\n"
        "/start — приветствие и инструкция\n"
        "/help — эта справка\n"
        "/set\_city <город> — сохранить город\n"
        "/my\_city — показать сохранённый город\n"
        "/weather — погода по сохранённому городу\n\n"
        "*Примеры:*\n"
        "/set\_city Москва\n"
        "/my\_city\n"
        "/weather\n"
        "погода Лондон\n"
        "погода Париж",
        parse_mode="Markdown"
    )
