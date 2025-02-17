# import requests
# from aiogram import types

# def search_music(query):
#     # Замените 'YOUR_LASTFM_API_KEY' на ваш ключ API
#     url = f"https://ws.audioscrobbler.com/2.0/?method=track.search&track={query}&api_key=1a2d7b5ffdecddcf654aa5bc20102a2a&format=json"
#     response = requests.get(url).json()

#     # Извлекаем данные о треках
#     tracks = response['results']['trackmatches']['track']
    
#     # Возвращаем только необходимые данные
#     music_data = []
#     for track in tracks[:10]:  # Ограничим результат первыми 10 резулaтатами
#         stream_url = None
#         # Проверяем, является ли streamable словарем, а не строкой
#         if isinstance(track.get('streamable'), dict):
#             stream_url = track.get('streamable', {}).get('#text', None)
        
#         music_data.append({
#             'name': f"{track['name']} - {track['artist']}",
#             'url': track['url'],  # Ссылка на трек на Last.fm
#             'stream_url': stream_url,  # Добавляем ссылку для прослушивания
#             'download_url': track.get('url', None)  # Ссылка для скачивания
#         })
    
#     return music_data


# # Функция для формирования инлайн кнопок с музыкой
# def create_music_buttons(results):
#     inline_buttons = []
#     for result in results:
#         name = result['name']
#         track_url = result['url']
#         stream_url = result.get('stream_url')
#         download_url = result.get('download_url')
        
#         # Формируем кнопки с действиями
#         buttons = []
        
#         if stream_url:
#             buttons.append(types.InlineKeyboardButton(text="Слушать", url=stream_url))
        
#         if download_url:
#             buttons.append(types.InlineKeyboardButton(text="Скачать", url=download_url))
        
#         inline_buttons.append(types.InlineKeyboardButton(text=name, url=track_url))
        
#         if buttons:
#             inline_buttons.append(*buttons)
    
#     inline_keyboard = types.InlineKeyboardMarkup(row_width=1).add(*inline_buttons)
#     return inline_keyboard
