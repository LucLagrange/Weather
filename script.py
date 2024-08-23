import requests
import logging
import os
import json
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_MAP_API_KEY = os.getenv("")
LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")

# Configure the logging module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Extracts the current weather
def get_current_weather(LATITUDE, LONGITUDE, OPEN_WEATHER_MAP_API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={OPEN_WEATHER_MAP_API_KEY}"
    logging.info("Fetching the weather information")

    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching the weather data:", e)
        return None


def extract_weather_information_from_json(data):

    # Initialize the JSON result
    weather_info = {
        "weather": None,
        "description": None,
        "temperature": None,
        "temperature_felt": None,
        "humidity": None,
        "date": None,
    }
    # Extract the information from the
    weather_info["weather"] = data["weather"][0].get(
        "main", "No weather data available"
    )
    weather_info["description"] = data["weather"][0].get(
        "description", "No description available"
    )
    #
    weather_info["temperature"] = data.get("main", {}).get(
        "temp", "No temperature avaible"
    )

    print(weather_info)


with open("weather.json", "r") as f:
    data = json.load(f)

extract_weather_information_from_json(data)
