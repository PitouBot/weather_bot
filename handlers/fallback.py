import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()

@router.message()
async def fallback(message: Message):
    await message.answer(
        "❌ Я не понял.\n"
        "Используй /help для списка команд\n\n"
        "🌍 Примеры запросов погоды:\n"
        "погода Москва\n"
        "погода Лондон"
    )