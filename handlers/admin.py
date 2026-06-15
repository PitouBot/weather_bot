import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import ADMINS
from models import UserCity


logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("del_user"))
async def admin_delete_user(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("⛔ У вас нет прав на эту команду")
        return
    
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("❌ Используйте: /del_user telegram_id")
        return
    
    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("❌ ID должен быть числом")
        return
    
    if UserCity.delete(user_id):
        await message.answer(f"✅ Пользователь {user_id} удалён из базы")
    else:
        await message.answer(f"❌ Пользователь {user_id} не найден")
