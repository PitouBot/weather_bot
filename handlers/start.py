import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🌤️ Привет! Я бот погоды.\n\n"
        "📋 *Доступные команды:*\n"
        "/set\_city Москва — сохранить город\n"
        "/my\_city — показать сохранённый город\n"
        "/weather — погода по сохранённому городу\n"
        "/help — полная справка\n\n"
        "🌍 Или просто напиши:\n"
        "погода Москва\n"
        "погода Лондон",
        parse_mode="Markdown"
    )
