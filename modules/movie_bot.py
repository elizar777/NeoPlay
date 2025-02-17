import requests
from config import TMDB_API_KEY

def get_movie_info(movie_name):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}&language=ru-RU'
    response = requests.get(url)
    data = response.json()

    if data['results']:
        # Разделяем название на слова
        words_in_query = movie_name.split()
            
        if len(words_in_query) == 1:  # Если запрос состоит из одного слова
            # Ищем точное совпадение по названию
            for movie in data['results']:
                if movie_name.lower() == movie['title'].lower():
                    movie_title = movie.get('title', 'Нет названия')
                    movie_year = movie.get('release_date', 'Нет даты релиза').split('-')[0]
                    movie_rating = movie.get('vote_average', 'Нет рейтинга')
                    movie_description = movie.get('overview', 'Нет описания')
                    movie_id = movie.get('id', '')  # Получаем ID фильма
                    movie_url = f'https://www.themoviedb.org/movie/{movie_id}'  # Ссылка на фильм

                    return (f"🎬 Название: {movie_title}\n"
                            f"📅 Год: {movie_year}\n"
                            f"⭐ Рейтинг: {movie_rating}\n"
                            f"📝 Описание: {movie_description}\n"
                            f"🔗 Ссылка: {movie_url}")
            
            # Если точного совпадения нет, выбираем первое совпадение
            best_match = data['results'][0]
        else:
            # Для запросов из нескольких слов берем первое совпадение
            best_match = data['results'][0]
        
        # Если точного совпадения не нашли, выводим информацию о первом найденном фильме
        movie_title = best_match.get('title', 'Нет названия')
        movie_year = best_match.get('release_date', 'Нет даты релиза').split('-')[0]
        movie_rating = best_match.get('vote_average', 'Нет рейтинга')
        movie_description = best_match.get('overview', 'Нет описания')
        movie_id = best_match.get('id', '')  # Получаем ID фильма
        movie_url = f'https://www.themoviedb.org/movie/{movie_id}'  # Ссылка на фильм

        return (f"🎬 Название: {movie_title}\n"
                f"📅 Год: {movie_year}\n"
                f"⭐ Рейтинг: {movie_rating}\n"
                f"📝 Описание: {movie_description}\n"
                f"🔗 Ссылка: {movie_url}")
    else:
        return "❌ Фильм не найден. Попробуйте другое название."
