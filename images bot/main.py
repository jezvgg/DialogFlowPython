from aiogram import Bot, Dispatcher, executor
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
    res = ""
    if len(response.query_result.fulfillment_messages) != 0:
        payload = dict(response.query_result.fulfillment_messages[1].payload)
        res = payload['url']
    await bot.send_message(chat_id=message.chat.id,text=f'{response.query_result.fulfillment_text}<a href="{res}">!</a>', parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp)