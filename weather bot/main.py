from aiogram import Bot, Dispatcher, executor
from google.cloud import dialogflow
from geopy.geocoders import Nominatim
from pyowm import OWM
from pathlib import Path
import json

settings_file = open(Path('settings.json')) # Загружаем json файл с настройками
settings = json.load(settings_file)

bot = Bot(token=settings['bot-token']) # Создаём бота
dp = Dispatcher(bot)

owm = OWM(settings['owm-key']) # Создаём менеджер для работы с OWM Api
manager = owm.weather_manager()
geolocator = Nominatim(user_agent='weather-bot') # Для перевода из строки в ширину и долготу, для погоды

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

    if response.query_result.intent.display_name == "погода" and response.query_result.all_required_params_present:
        city = dict(dict(response.query_result.parameters)['location'])['city']
        location = geolocator.geocode(city)
        weather_location = manager.weather_at_coords(location.latitude, location.longitude)
        weather = weather_location.weather
        answer = f"Temperature: {weather.temperature('celsius')['temp']} C`, {weather.detailed_status}"
        await message.answer(answer)

    else:
        await message.answer(response.query_result.fulfillment_text)


if __name__ == '__main__':
    executor.start_polling(dp)