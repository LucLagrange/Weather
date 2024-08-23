import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_MAP_API_KEY = os.getenv("")
LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")


# Extracts the current weather
def get_current_weather(LATITUDE, LONGITUDE, OPEN_WEATHER_MAP_API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={OPEN_WEATHER_MAP_API_KEY}"

    response = requests.get(url)

    data = response.json()

    print(data)


get_current_weather(LATITUDE, LONGITUDE, OPEN_WEATHER_MAP_API_KEY)
