from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from google.cloud import dialogflow
from pathlib import Path
import json

settings_file = open(Path('settings.json')) # Загружаем json файл с настройками
settings = json.load(settings_file)

bot = Bot(token=settings['bot-token'])
dp = Dispatcher(bot)

project_id = settings['project_id'] # Записываем настройки
session_id = settings['session_id']
language = settings['language']

session_client = dialogflow.SessionsClient()                # Создание сессии
session = session_client.session_path(project_id, session_id)


@dp.message_handler()
async def start(message):
    text = message.text

    text_input = dialogflow.TextInput(text=text, language_code=language) # Ввод текста
    query_input = dialogflow.QueryInput(text=text_input) # Запрос к агенту по тексту
    response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )

    if len(response.query_result.fulfillment_messages) != 1: # если payload нет, то будет текст и длина 1
        payload = dict(response.query_result.fulfillment_messages[1].payload) # custom payload интента

        if 'keyboard' in payload.keys(): # Проходим по всем кнопкам и созда1м клавиатуру
            keyboard = InlineKeyboardMarkup()
            for buttons in dict(payload['keyboard']).values():
                button = dict(buttons)
                print(button)
                if "url" in button.keys():
                    keyboard.add(InlineKeyboardButton(text=button['text'], url=button['url'])) # Кнопки с ссылками
                elif "data" in button.keys():
                    keyboard.add(InlineKeyboardButton(text=button['text'], callback_data=button['data'])) # Кнопки с data

        await message.answer(response.query_result.fulfillment_text, reply_markup=keyboard)

    else:
        await message.answer(response.query_result.fulfillment_text)


# Оработка кнопки с data
@dp.callback_query_handler(text='data')
async def callback(callback):
    await callback.message.answer('Кэллбэк обработан')


if __name__ == '__main__':
    executor.start_polling(dp)