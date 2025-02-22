import aiohttp
from config import API_KEY_WEATHER

async def get_weather(city):
    url = f'https://api.weatherapi.com/v1/forecast.json?q={city}&key={API_KEY_WEATHER}&days=7&lang=ru'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                forecast = data.get('forecast', {}).get('forecastday', [])

                weather_info = ""

                for day in forecast:
                    date = day['date']  # Получаем дату в формате YYYY-MM-DD
                    temp = round(day['day']['avgtemp_c'], 1)
                    description = day['day']['condition']['text']

                    # Преобразуем дату в формат "DD.MM"
                    year, month, day_num = date.split('-')  # Меняем порядок частей
                    formatted_date = f"{day_num}.{month}"  # Теперь будет "22.02"

                    weather_info += f"{formatted_date} — 🌡 {temp}°C, {description}\n"

                return weather_info.strip()

            return "❗ Ошибка при получении погоды. Попробуйте позже."
