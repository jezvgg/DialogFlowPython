from aiogram import Bot, Dispatcher, executor
from pathlib import Path
from settings import settings
from dialogflow import response
from sheets import sheets

settings = settings(Path('settings.json'))

bot = Bot(settings.bot_token)
dp = Dispatcher(bot)

sheet = sheets(settings)

@dp.message_handler()
async def main(message):
    result = response(settings, message.text)
    params = dict(result.query_result.parameters)
    intent = result.query_result.intent.display_name
    if intent == 'Совет книги': # книга
        await message.answer(sheet.get_books(params['genres']))
    elif intent == 'Совет фильма': # фильм
        await message.answer(sheet.get_movies(params['genres'], params['emortions']))
    else:
        await message.answer(result.query_result.fulfillment_text)

if __name__ == '__main__':
    executor.start_polling(dp)