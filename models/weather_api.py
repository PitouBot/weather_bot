import aiohttp
import logging
from config import WEATHER_API_KEY, WEATHER_API_URL

logger = logging.getLogger(__name__)

class WeatherAPI:
    API_KEY = WEATHER_API_KEY
    BASE_URL = WEATHER_API_URL

    @classmethod
    async def get_weather(cls, city: str) -> str:
        params = {
            'q': city,
            'appid': cls.API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(cls.BASE_URL, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return True, cls._format_weather(data)
                    elif resp.status == 404:
                        return False, f"❌ Город '{city}' не найден"
                    else:
                        logger.warning(f"Weather API error: {resp.status}")
                        return False, "❌ Сервис погоды временно недоступен"
            except aiohttp.ClientError as e:
                logger.error(f"Network error: {e}")
                return False, "❌ Ошибка подключения к сервису погоды"
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return False, "❌ Непредвиденная ошибка"

    @staticmethod
    def _format_weather(data: dict) -> str:
        name = data['name']
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        description = data['weather'][0]['description'].capitalize()
        
        return (
            f"🌍 Город: {name}\n"
            f"🌡️ Температура: {temp}°, ощущается как {feels_like}°\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind} м/с\n"
            f"📖 {description}"
        )