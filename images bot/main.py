from aiogram import Bot, Dispatcher, executor
from dialogflow import DialogFlowHelper
from pathlib import Path
import json


# Upload settings file
settings_file = open(Path('settings.json'))
settings = json.load(settings_file)
helper = DialogFlowHelper('settings.json')


bot = Bot(token=settings['bot-token'])
dp = Dispatcher(bot)


@dp.message_handler()
async def start(message):
    # Same response as simple example
    text = message.text
    response = helper.response(text=text)

    # Getting custom payload and parsing him for images
    if len(response.query_result.fulfillment_messages) != 0:
        payload = dict(response.query_result.fulfillment_messages[1].payload)
        res = payload['url']
    await bot.send_message(chat_id=message.chat.id,text=f'{response.query_result.fulfillment_text}<a href="{res}">!</a>', parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp)