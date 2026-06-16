import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import main_menu


logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🌤️ Привет! Я бот погоды.\n\n"
        "👇 Используй кнопки меню или команды (список команд доступен через /help):",
        reply_markup=main_menu
    )

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "📋 Главное меню:",
        reply_markup=main_menu
    )
