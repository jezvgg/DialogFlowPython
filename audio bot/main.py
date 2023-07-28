from aiogram import Bot, Dispatcher, executor
from aiogram.types import ContentType
from google.cloud import dialogflow
import speech_recognition as s_r
from gtts import gTTS
import soundfile as sf
from pathlib import Path
import json
import os
from speech import STT, TTS
from dialogflow import DialogFlowHelper


# Upload settings files
settings_file = open(Path('settings.json'))
settings = json.load(settings_file)
helper = DialogFlowHelper(settings='settings.json')


bot = Bot(token=settings['bot-token'])
dp = Dispatcher(bot)


@dp.message_handler(content_types=[ContentType.VOICE])
async def audio(message):
    # Download audio file
    file_id = await bot.get_file(message.voice.file_id)
    print(file_id.file_path)
    await bot.download_file(file_id.file_path, 'audio.oga')
    print('Audio saved')

    # Speech-to-Text convertation
    text = STT('audio.oga')
    
    # Response for DialogFlow ( same in simple example )
    text_output = helper.response_for_text(text=text)

    # Text-to-Speech convertation
    audio_path = TTS(text=text_output)

    # Send Speech of response
    with open(audio_path, 'rb') as output:
        await bot.send_audio(chat_id=message.chat.id, audio=output)
    os.remove(audio_path)
    await bot.send_message(chat_id=message.chat.id,text=text_output)


@dp.message_handler(content_types=[ContentType.TEXT])
async def start(message):
    text = message.text
    print('audio not detected')

    await bot.send_message(chat_id=message.chat.id,text=helper.response_for_text(text=text))


if __name__ == '__main__':
    executor.start_polling(dp)