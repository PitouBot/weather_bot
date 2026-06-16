import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline import main_menu

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


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📋 Команды:\n/start — меню\n/set_city — установить город\n/my_city — показать город\n/weather — погода",
        reply_markup=main_menu
    )