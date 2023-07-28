from aiogram import Bot, Dispatcher, executor
from aiogram.types import ContentType
from google.cloud import dialogflow
import speech_recognition as s_r
from gtts import gTTS
import soundfile as sf
from pathlib import Path
import json
import os

settings_file = open(Path('settings.json')) # Загружаем json файл с настройками
settings = json.load(settings_file)

bot = Bot(token=settings['bot-token'])
dp = Dispatcher(bot)

project_id = settings['project-id'] # Записываем настройки
session_id = settings['session-id']
language = settings['language']

session_client = dialogflow.SessionsClient()                # Создание сессии
session = session_client.session_path(project_id, session_id)


@dp.message_handler(content_types=[ContentType.VOICE])
async def audio(message):
    file_id = await bot.get_file(message.voice.file_id)
    print(file_id.file_path)
    await bot.download_file(file_id.file_path, 'audio.oga')
    print('Audio saved')

    data, sample = sf.read('audio.oga')
    sf.write('audio.wav', data, sample)
    print('Audio exported to WAV')

    recognaizer = s_r.Recognizer()
    audio_file = s_r.AudioFile('audio.wav')
    with audio_file as source:
        recognaizer.adjust_for_ambient_noise(source)
        recorded_audio = recognaizer.listen(source)
    print('Audio cleaned')

    alt = recognaizer.recognize_google(
        recorded_audio,
        language='ru-RU',
        show_all=True
     )
    try:
        text = alt['alternative'][0]['transcript']
    except TypeError:
        print('typeError')
        text = 'Не получилось разобрать аудиосообщение, отправитье пожалуйста ещё раз. Желательно с задержкой в начале.'

    print('Audio recognized')
    os.remove('audio.oga')
    os.remove('audio.wav')
    
    text_input = dialogflow.TextInput(text=text, language_code=language) # Ввод текста
    query_input = dialogflow.QueryInput(text=text_input) # Запрос к агенту по тексту
    response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )


    text_output = response.query_result.fulfillment_text
    obj = gTTS(text = text_output, lang='ru', slow=False)
    obj.save('output.mp3')
    output = open('output.mp3', 'rb')
    await bot.send_audio(chat_id=message.chat.id, audio=output)
    output.close()
    os.remove('output.mp3')

    await bot.send_message(chat_id=message.chat.id,text=response.query_result.fulfillment_text)


@dp.message_handler(content_types=[ContentType.TEXT])
async def start(message):
    text = message.text
    print('audio not detected')
    text_input = dialogflow.TextInput(text=text, language_code=language) # Ввод текста
    query_input = dialogflow.QueryInput(text=text_input) # Запрос к агенту по тексту
    response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )

    await bot.send_message(chat_id=message.chat.id,text=response.query_result.fulfillment_text)


if __name__ == '__main__':
    executor.start_polling(dp)