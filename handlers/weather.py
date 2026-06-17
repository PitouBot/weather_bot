import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.form import Form
from models import UserCity, WeatherAPI
from keyboards.inline import main_menu


logger = logging.getLogger(__name__)
router = Router()

# === КОМАНДЫ ===
@router.message(Command("set_city"))
async def cmd_set_city(message: Message):
    city = message.text.replace("/set_city", "", 1).strip()
    if not city:
        await message.answer("❌ Укажи город: /set_city Москва")
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    success, result = await WeatherAPI.get_weather(city)

    if not success:
        await message.answer(result)
        return

    UserCity.set(message.from_user.id, city)
    await message.answer(f"✅ Город '{city}' сохранён!\n\n{result}", reply_markup=main_menu)


@router.message(Command("my_city"))
async def cmd_my_city(message: Message):
    city = UserCity.get(message.from_user.id)
    if city is None:
        await message.answer("❌ Город не установлен. Используй /set_city", reply_markup=main_menu)
        return
    await message.answer(f"🌍 Твой город: {city}", reply_markup=main_menu)


@router.message(Command("weather"))
async def cmd_weather(message: Message):
    city = UserCity.get(message.from_user.id)
    if city is None:
        await message.answer("❌ Город не установлен. Используй /set_city", reply_markup=main_menu)
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    _, result = await WeatherAPI.get_weather(city)
    await message.answer(result, reply_markup=main_menu)


# === ТЕКСТОВЫЙ ЗАПРОС ПОГОДЫ ===
@router.message(F.text.lower().startswith("погода "))
async def weather_in_city(message: Message):
    city = message.text.lower().replace('погода ', '', 1).strip()

    await message.bot.send_chat_action(message.chat.id, "typing")
    _, result = await WeatherAPI.get_weather(city)  
    await message.answer(result)


# === КНОПКИ (CALLBACK) ===
@router.callback_query(F.data == "set_city")
async def set_user_city(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Form.city) 
    await callback.message.edit_text(
        "📝 Напиши свой город:\n"
        "Например: Москва",     
        reply_markup=main_menu
    )


@router.callback_query(F.data == "my_city")
async def callback_my_city(callback: CallbackQuery):
    await callback.answer()
    city = UserCity.get(callback.from_user.id)
    if city is None:
        await callback.message.edit_text("❌ Город не установлен", reply_markup=main_menu)
        return
    await callback.message.edit_text(f"🌍 Твой город: {city}", reply_markup=main_menu)


@router.callback_query(F.data == "weather")
async def callback_weather(callback: CallbackQuery):
    await callback.answer()
    city = UserCity.get(callback.from_user.id)
    if city is None:
        await callback.message.edit_text("❌ Город не установлен. Нажми 'Установить город'", reply_markup=main_menu)
        return

    await callback.message.bot.send_chat_action(callback.message.chat.id, "typing")
    _, result = await WeatherAPI.get_weather(city)
    await callback.message.edit_text(result, reply_markup=main_menu)


# === ОБРАБОТКА ВВОДА ГОРОДА (FSM) ===
@router.message(Form.city)
async def handle_city_input(message: Message, state: FSMContext):
    city = message.text.strip()

    await message.bot.send_chat_action(message.chat.id, "typing")
    success, result = await WeatherAPI.get_weather(city)

    if not success:
        await message.answer(f"❌ Город '{city}' не найден. Попробуй ещё раз.")
        return

    UserCity.set(message.from_user.id, city)
    await state.clear()  # ← сбрасываем состояние 
                    
    await message.answer(
        f"✅ Город '{city}' сохранён!\n\n{result}",
        reply_markup=main_menu
    )



    