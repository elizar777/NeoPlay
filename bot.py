from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging, time, sqlite3

# Настройки бота
from config import API_TOKEN
from modules.movie_bot import get_movie_info
from modules.weather import get_weather

logging.basicConfig(level=logging.INFO)

# Подключение к базе данных
connection = sqlite3.connect('customer.db')
cursor = connection.cursor()

# Создание таблицы пользователей
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        username VARCHAR(100),
        date_joined VARCHAR(100)
    );
""")
cursor.connection.commit()

# Состояния FSM
class Form(StatesGroup):
    waiting_for_movie = State()  # Поиск фильма
    waiting_for_city = State()  # Выбор города для погоды

# Создание бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Клавиатуры
start_keyboard = [
    types.KeyboardButton("Фильмы"),
    types.KeyboardButton("Гороскоп"),
    types.KeyboardButton("Погода"),
    types.KeyboardButton("Загадки")
]
start_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboard)

city_keyboard = [
    types.KeyboardButton("Бишкек"), types.KeyboardButton("Ош"), types.KeyboardButton("Джалал-Абад"),
    types.KeyboardButton("Каракол"), types.KeyboardButton("Нарын"), types.KeyboardButton("Талас"),
    types.KeyboardButton("Баткен")
]
city_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*city_keyboard)

# Словарь перевода городов
city_dict = {
    "Бишкек": "Bishkek",
    "Ош": "Osh",
    "Джалал-Абад": "Jalal-Abad",
    "Каракол": "Karakol",
    "Нарын": "Naryn",
    "Талас": "Talas",
    "Баткен": "Batken"
}

def get_city_english(city_name):
    return city_dict.get(city_name, city_name)

# Команда /start
@dp.message_handler(commands='start')
async def start(message: types.Message):
    cursor.execute("SELECT id FROM users WHERE id = ?", (message.from_user.id,))
    user_exists = cursor.fetchone()
    
    if not user_exists:
        cursor.execute("""INSERT INTO users (id, first_name, last_name, username, date_joined)
                          VALUES (?, ?, ?, ?, ?)""", (
            message.from_user.id, message.from_user.first_name,
            message.from_user.last_name, message.from_user.username,
            time.ctime()
        ))
        cursor.connection.commit()

    await message.answer(f"Здравствуйте, {message.from_user.full_name}! Ваши данные сохранены.", reply_markup=start_button)

# Обработчик "Фильмы"
@dp.message_handler(text='Фильмы')
async def films(message: types.Message):
    await Form.waiting_for_movie.set()
    await message.reply("❗ Введите название фильма:")

@dp.message_handler(state=Form.waiting_for_movie)
async def cmd_movie(message: types.Message, state: FSMContext):
    movie_name = message.text.strip()
    if not movie_name:
        await message.reply("❗ Укажите название фильма.")
        return

    movie_info = get_movie_info(movie_name)
    await message.reply(movie_info, reply_markup=start_button)
    await state.finish()

# Обработчик "Погода"
@dp.message_handler(text='Погода')
async def weather(message: types.Message):
    await Form.waiting_for_city.set()
    await message.reply("Выберите город:", reply_markup=city_markup)

@dp.message_handler(state=Form.waiting_for_city)
async def cmd_weather(message: types.Message, state: FSMContext):
    city = message.text.strip()

    if city not in city_dict:
        await message.reply("❗ Выберите город из списка.")
        return

    city_en = get_city_english(city)
    weather_text = await get_weather(city_en)
    
    await message.reply(weather_text, reply_markup=start_button)
    await state.finish()

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
