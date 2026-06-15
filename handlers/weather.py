import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from models import UserCity, WeatherAPI

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command('set_city'))
async def set_user_city(message: Message):
    city = message.text.replace('/set_city', '', 1).strip()

    if not city:
        await message.answer("❌ Укажи город: /set_city Москва")
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    success, result = await WeatherAPI.get_weather(city)

    if not success:
        await message.answer(result)  
        return
    
    UserCity.set(message.from_user.id, city)
    await message.answer(f"✅ Город '{city}' сохранён!\n\n{result}")

@router.message(Command('my_city'))
async def my_city(message: Message):
    city = UserCity.get(message.from_user.id)
    if city is None:
        await message.answer(
            "❌ У вас не установлен город!\n"
            "Укажите город с помощью команды /set_city\n"
            "Например: /set_city Москва\n"
            )
        return
    
    await message.answer(f"Ваш город {city}")

@router.message(Command('weather'))
async def weather(message: Message):
    city = UserCity.get(message.from_user.id)  
    if city is None:
        await message.answer(
            "❌ У вас не установлен город!\n"
            "Укажите город с помощью команды /set\_city\n"
            "Например: /set\_city Москва\n"
            "Или просто напишите так:\n"
            "погода Москва"
            )
        return
    
    await message.bot.send_chat_action(message.chat.id, "typing")
    _, result = await WeatherAPI.get_weather(city)  
    await message.answer(result)

@router.message(F.text.lower().startswith("погода "))
async def weather_in_city(message: Message):
    city = message.text.lower().replace('погода ', '', 1).strip()

    await message.bot.send_chat_action(message.chat.id, "typing")
    _, result = await WeatherAPI.get_weather(city)  
    await message.answer(result)


