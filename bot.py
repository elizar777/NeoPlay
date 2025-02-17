from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import logging, time, sqlite3

# Настройки бота
from config import API_TOKEN
from modules.movie_bot import get_movie_info
from modules.music_bot import search_music, create_music_buttons

logging.basicConfig(level=logging.INFO)

# Создаем подключение к базе данных
connection = sqlite3.connect('customer.db')
cursor = connection.cursor()

# Создаем таблицу пользователей, если её нет
cursor.execute(f"""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    date_joined VARCHAR(100)
);""")
cursor.connection.commit()

# Состояния FSM
class Form(StatesGroup):
    waiting_for_movie = State()  # Ожидание запроса фильма
    waiting_for_music = State()  # Ожидание запроса музыки

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


start_keyboard = [
    types.KeyboardButton("Фильмы"),
    types.KeyboardButton("Музыка"),
    types.KeyboardButton("Погода"),
    types.KeyboardButton("Загадки")
]

start_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_keyboard)

# Обработчик команды /start
@dp.message_handler(commands='start')
async def start(message: types.Message):
    cursor.execute("SELECT id FROM users WHERE id = ?", (message.from_user.id,))
    output_cursor = cursor.fetchall()
    if not output_cursor:
        cursor.execute("""INSERT INTO users (id, first_name, last_name, username, date_joined)
                          VALUES (?, ?, ?, ?, ?)""", (
            message.from_user.id, message.from_user.first_name,
            message.from_user.last_name, message.from_user.username,
            time.ctime()
        ))
        cursor.connection.commit()
    await message.answer(f"Здравствуйте, {message.from_user.full_name}! Ваши данные сохранены в базе данных.", reply_markup=start_button)

# Обработчик кнопки "Фильмы"
@dp.message_handler(text='Фильмы')
async def films(message: types.Message):
    await Form.waiting_for_movie.set()  # Переход в состояние поиска фильма
    await message.reply("❗ Напишите название фильма, который вы хотите найти:")

# Обработчик получения названия фильма
@dp.message_handler(state=Form.waiting_for_movie)
async def cmd_movie(message: types.Message, state: FSMContext):
    movie_name = message.text.strip()  # Получаем название фильма
    if not movie_name:
        await message.reply("❗ Пожалуйста, укажите название фильма.")
        return

    movie_info = get_movie_info(movie_name)
    await message.reply(movie_info, reply_markup=start_button)
    await state.finish()  # Завершаем состояние


# Обработчик кнопки "Музыка"
@dp.message_handler(text='Музыка')
async def music(message: types.Message):
    await Form.waiting_for_music.set()  # Переход в состояние поиска музыки
    await message.reply("❗ Напишите название песни или исполнителя, чтобы начать поиск.")
    
    
# Обработчик получения запроса для поиска музыки
@dp.message_handler(state=Form.waiting_for_music)
async def handle_music_query(message: types.Message, state: FSMContext):
    query = message.text.strip()
    if not query:
        await message.reply("❗ Пожалуйста, укажите название песни или исполнителя.")
        return

    # Получаем данные о треках
    results = search_music(query)
    
    if results:
        # Создаем инлайн кнопки для каждого найденного результата
        inline_keyboard = create_music_buttons(results)
        
        await message.reply("Вот результаты по запросу:", reply_markup=inline_keyboard)
    else:
        await message.reply("❗ Ничего не найдено по вашему запросу.")
    
    await state.finish()  # Завершаем состояние


# Запуск бота
executor.start_polling(dp, skip_updates=True)
