from aiogram import Bot, Dispatcher, executor
from pathlib import Path
from settings import settings
from dialogflow import response
from sheets import sheets

settings = settings(Path('settings.json')) # Создаём класс с настройками

bot = Bot(settings.bot_token) # Создаём бота
dp = Dispatcher(bot)

sheet = sheets(settings) # класс для работы с Google Sheets

@dp.message_handler()
async def main(message):
    result = response(settings, message.text) # Запрос к DialogFlow
    params = dict(result.query_result.parameters) # Параметры от DialogFlow 
    intent = result.query_result.intent.display_name # Интент, который определил DialogFlow
    if intent == 'Совет книги': 
        await message.answer(sheet.get_books(params['genres']))
        settings.last_params = params
        settings.counter = 0
    elif intent == 'Совет фильма': 
        await message.answer(sheet.get_movies(params['genres'], params['emortions']))
        settings.last_params = params
        settings.counter = 0
    elif intent == 'а ещё фильмы':
        settings.counter += 1
        await message.answer(sheet.get_movies(settings.last_params['genres'], settings.last_params['emortions']))
    elif intent == 'ещё книги':
        settings.counter += 1
        await message.answer(sheet.get_movies(settings.last_params['genres']))
    else:
        await message.answer(result.query_result.fulfillment_text) # Если не нужен совет, то отвечает DialogFlow, иначе мы сами отвечаем.
        settings.counter = 0

if __name__ == '__main__':
    executor.start_polling(dp) # Запуск бота