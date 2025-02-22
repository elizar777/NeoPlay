import aiohttp
from bs4 import BeautifulSoup

async def get_news_from_24kg():
    url = 'https://24.kg/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')

                # Находим все элементы с классом 'title'
                news_titles = soup.find_all('div', class_='title')

                news_text = "📰 Новости с сайта 24.kg:\n\n"
                for i, title_div in enumerate(news_titles[:8]):
                    # Находим ссылку внутри элемента 'title'
                    link_tag = title_div.find('a')
                    if link_tag:
                        title = link_tag.get_text(strip=True)
                        link = link_tag['href']
                        # Добавляем смайлики и улучшенный формат
                        news_text += f"🔹 {title}\n\n"
                    else:
                        continue  # Пропускаем элемент, если нет ссылки

                news_text += "🔗 Ссылка на сайт 24.kg: [https://24.kg/](https://24.kg/)"
                return news_text
            else:
                return "❗ Ошибка при получении новостей."
