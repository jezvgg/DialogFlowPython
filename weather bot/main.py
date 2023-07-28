from aiogram import Bot, Dispatcher, executor
from google.cloud import dialogflow
from geopy.geocoders import Nominatim
from pyowm import OWM
from ..utils.dialogflow import DialogFlowHelper
from pathlib import Path
import json


# Upload settings file
settings_file = open(Path('settings.json'))
settings = json.load(settings_file)
helper = DialogFlowHelper(settings='settings.json')


bot = Bot(token=settings['bot-token'])
dp = Dispatcher(bot)

# Manager for work with OpenWeatherMap
owm = OWM(settings['owm-key'])
manager = owm.weather_manager()
geolocator = Nominatim(user_agent='weather-bot') # For convert to longitude and latitude


@dp.message_handler()
async def start(message):
    # Same response that in simple example
    text = message.text
    response = helper.response(text=text)

    if response.query_result.intent.display_name == "погода" and response.query_result.all_required_params_present:
        city = dict(dict(response.query_result.parameters)['location'])['city'] # Take city parameter from DF response
        location = geolocator.geocode(city)
        weather_location = manager.weather_at_coords(location.latitude, location.longitude)
        weather = weather_location.weather
        answer = f"Temperature: {weather.temperature('celsius')['temp']} C`, {weather.detailed_status}"
        await message.answer(answer)

    else:
        await message.answer(response.query_result.fulfillment_text) # Not asking for a weather


if __name__ == '__main__':
    executor.start_polling(dp)