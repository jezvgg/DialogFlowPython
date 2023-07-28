from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..utils.dialogflow import DialogFlowHelper
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

    # Same response that in simple example
    text = message.text
    response = helper.response(text=text)

    if len(response.query_result.fulfillment_messages) != 1: # If length is 1, then there is no payload
        # Intent custom payload
        payload = dict(response.query_result.fulfillment_messages[1].payload)

        # Parse all buttons and create a keyboard
        if 'keyboard' in payload.keys():
            keyboard = InlineKeyboardMarkup()
            for buttons in dict(payload['keyboard']).values():
                button = dict(buttons)
                print(button)
                if "url" in button.keys():
                    keyboard.add(InlineKeyboardButton(text=button['text'], url=button['url'])) # Buttons with urls
                elif "data" in button.keys():
                    keyboard.add(InlineKeyboardButton(text=button['text'], callback_data=button['data'])) # Buttons with callback_data

        await message.answer(response.query_result.fulfillment_text, reply_markup=keyboard)

    else:
        await message.answer(response.query_result.fulfillment_text)


# Оработка кнопки с data
@dp.callback_query_handler(text='data')
async def callback(callback):
    await callback.message.answer('Callback done.')


if __name__ == '__main__':
    executor.start_polling(dp)