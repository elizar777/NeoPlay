import aiohttp
from config import API_KEY_HOROSCOPE

async def get_horoscope(sign):
    url = f'https://freeastrologyapi.com/api/horoscope/{sign}/today'
    headers = {
        'Authorization': f'Bearer {API_KEY_HOROSCOPE}',
        'User-Agent': 'TelegramBot/1.0'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('horoscope', 'Гороскоп не найден.')
            else:
                return 'Ошибка при получении гороскопа.'
