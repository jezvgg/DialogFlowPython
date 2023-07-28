from aiogram import Bot, Dispatcher, executor
from google.cloud import dialogflow
from pathlib import Path
import json

# upload settings file
settings_file = open(Path('settings.json'))
settings = json.load(settings_file)

bot = Bot(token=settings['bot-token'])
dp = Dispatcher(bot)

# create session to work with DialogFlow
session_client = dialogflow.SessionsClient()                
session = session_client.session_path(settings['project_id'] , settings['session_id'])


@dp.message_handler()
async def start(message):
    text = message.text

    # response from simple example
    text_input = dialogflow.TextInput(text=text, language_code="RU")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )

    await message.answer(response.query_result.fulfillment_text)


if __name__ == '__main__':
    executor.start_polling(dp)