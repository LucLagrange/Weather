import requests
import logging
import os
import datetime
from timeit import default_timer as timer
from google.cloud import bigquery

OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")
LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
TABLE_ID = os.getenv("TABLE_ID")

# Configure the logging module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Extracts the current weather
def get_current_weather(LATITUDE, LONGITUDE, OPEN_WEATHER_MAP_API_KEY):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}"
        f"&lon={LONGITUDE}&appid={OPEN_WEATHER_MAP_API_KEY}"
    )

    params = {
        "units": "metric",  # 'metric' for Celsius, 'imperial' for Fahrenheit
        "lang": "en",  # Language for the response
    }

    logging.info("Fetching the weather information for %s, %s", LATITUDE, LONGITUDE)

    try:
        response = requests.get(url, params=params)
        data = response.json()
        logging.info("Succesfuly fetched weather information")
        logging.info("API response: %s", data)
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching the weather data:", e)
        return None

    return data


def extract_weather_information_from_json(data):

    logging.info("Extracting weather information from the API response")

    # Initialize the JSON result
    weather_info = {
        "weather": None,
        "description": None,
        "temperature": None,
        "temperature_felt": None,
        "humidity": None,
        "wind_speed": None,
        "date": None,
    }

    # Extract the information from the API response
    try:
        weather_info["weather"] = data["weather"][0]["main"]
    except (IndexError, KeyError, TypeError) as e:
        logging.error("Failed to extract 'weather': %s", e)
        weather_info["weather"] = "No weather data available"

    try:
        weather_info["description"] = data["weather"][0]["description"]
    except (IndexError, KeyError, TypeError) as e:
        logging.error("Failed to extract 'description': %s", e)
        weather_info["description"] = "No description available"

    try:
        weather_info["temperature"] = data["main"]["temp"]
    except KeyError as e:
        logging.error("Failed to extract 'temperature': %s", e)
        weather_info["temperature"] = "No temperature available"

    try:
        weather_info["temperature_felt"] = data["main"]["feels_like"]
    except KeyError as e:
        logging.error("Failed to extract 'temperature_felt': %s", e)
        weather_info["temperature_felt"] = "No 'feels like' temperature available"

    try:
        weather_info["humidity"] = data["main"]["humidity"]
    except KeyError as e:
        logging.error("Failed to extract 'humidity': %s", e)
        weather_info["humidity"] = "No humidity data available"

    try:
        weather_info["wind_speed"] = data["wind"]["speed"]
    except KeyError as e:
        logging.error("Failed to extract 'wind_speed': %s", e)
        weather_info["wind_speed"] = "No wind speed data available"

    # Convert the timestamp to a readable local date
    try:
        timestamp = data["dt"]
        timezone_offset = data.get("timezone", 0)
        utc_time = datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
        local_time = utc_time + datetime.timedelta(seconds=timezone_offset)
        weather_info["date"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
    except (KeyError, TypeError) as e:
        logging.error("Failed to convert timestamp to date: %s", e)
        weather_info["date"] = "No date available"

    logging.info("Successfully extracted weather information: %s", weather_info)

    return weather_info


def append_weather_data_to_bigquery(weather_info, TABLE_ID):
    logging.info("Table ID is: %s", TABLE_ID)
    try:
        logging.info("Initializing BigQuery client.")
        client = bigquery.Client()

        # Check if client is correctly initialized
        if client is None:
            logging.error("Failed to initialize BigQuery client. Client is None.")
            return

        # Insert the rows into the table
        errors = client.insert_rows_json(TABLE_ID, [weather_info])

        if errors:
            raise Exception(f"BigQuery insertion errors occurred: {errors}")

        logging.info("Weather information successfully appended to BigQuery.")

    except Exception as e:
        logging.error("An error occurred while appending data to BigQuery: %s", e)


def main():
    start = timer()
    data = get_current_weather(LATITUDE, LONGITUDE, OPEN_WEATHER_MAP_API_KEY)
    weather_information = extract_weather_information_from_json(data)
    append_weather_data_to_bigquery(weather_information, TABLE_ID)
    end = timer()
    duration = round(end - start, 1)
    logging.info("The script took %ss to complete", duration)


if __name__ == "__main__":
    main()
