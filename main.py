from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список нежелательных слов (цензура)
BLACKLIST_WORDS = ['геншин', 'дурак', 'лох']  # Замените на свои слова

# Фильтр для проверки на нежелательные слова
def has_bad_words(text: str) -> bool:
    return any(word in text.lower() for word in BLACKLIST_WORDS)

# Фильтр для проверки на наличие цифр в тексте
def has_numbers(text: str) -> bool:
    return any(char.isdigit() for char in text)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nМеня зовут Эхо-бот!\n'
        'Я умею:\n'
        '- Повторять текст (/help для списка команд)\n'
        '- Фильтровать нежелательные слова\n'
        '- Проверять текст на наличие цифр\n'
        '- Работать со стикерами'
    )


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Доступные команды:\n'
        '/start - начать общение\n'
        '/help - справка\n'
        '/caps <текст> - перевести текст в верхний регистр\n'
        '/reverse <текст> - перевернуть текст\n\n'
        'Фильтры:\n'
        '- Автоматическая проверка на нежелательные слова\n'
        '- Проверка на наличие цифр в тексте\n\n'
        'Также можно отправить стикер или любой текст'
    )


# Этот хэндлер будет срабатывать на команду "/caps"
@dp.message(Command(commands=['caps']))
async def process_caps_command(message: Message):
    text = message.text[6:].strip()
    if text:
        if has_bad_words(text):
            await message.reply('Извините, ваш текст содержит недопустимые слова')
        else:
            await message.reply(text.upper())
    else:
        await message.reply('Пожалуйста, укажите текст после команды /caps')


# Этот хэндлер будет срабатывать на команду "/reverse"
@dp.message(Command(commands=['reverse']))
async def process_reverse_command(message: Message):
    text = message.text[9:].strip()
    if text:
        if has_bad_words(text):
            await message.reply('Извините, ваш текст содержит недопустимые слова')
        else:
            await message.reply(text[::-1])
    else:
        await message.reply('Пожалуйста, укажите текст после команды /reverse')


@dp.message(lambda message: message.sticker)
async def handle_sticker(message: Message):
    await message.reply("Крутой стикер! 😊 У меня бы тоже такой был, но я всего лишь бот...")


# Хэндлер для текста с цифрами
@dp.message(lambda message: message.text and has_numbers(message.text))
async def handle_text_with_numbers(message: Message):
    await message.reply("Ваше сообщение содержит цифры! 🔢")


# Хэндлер для текста с нежелательными словами
@dp.message(lambda message: message.text and has_bad_words(message.text))
async def handle_bad_words(message: Message):
    await message.reply("Извините, ваше сообщение содержит недопустимые слова 🚫")


# Этот хэндлер будет срабатывать на обычные текстовые сообщения
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)