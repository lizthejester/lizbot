# This example requires the 'message_content' intent.
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def get_weather() -> str:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 47.037872,
        "longitude": -122.900696,
        "current": ["temperature_2m", "relative_humidity_2m", "is_day", "weather_code"],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "dew_point_2m",
            "apparent_temperature",
            "precipitation_probability",
            "weather_code",
        ],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timeformat": "unixtime",
        "timezone": "Pacific/Auckland",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = str(round(current.Variables(0).Value(), 2))
    current_relative_humidity_2m = str(current.Variables(1).Value())
    current_is_day = current.Variables(2).Value()
    current_weather_code = int(current.Variables(3).Value())
    weather_codes = {
        0: "clear",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "foggy",
        48: "a depositing rime fog",
        51: "a light drizzle",
        53: "a moderate drizzle",
        55: "a dense drizzle",
        56: "a light freezing drizzle",
        57: "a dense freezing drizzle",
        61: "slightly rainy",
        63: "moderately rainy",
        65: "heavy rain",
        66: "light freezing rain",
        67: "heavy freezing rain",
        71: "slight snowfall",
        73: "moderate snowfall",
        75: "heavy snowfall",
        77: "snow grains",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        85: "slight snow showers",
        86: "heavy snow showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail",
    }

    # print(weathercode)
    print(weather_codes[current_weather_code])

    # print(f"Current time {current.Time()}")
    # print(f"Current temperature_2m {current_temperature_2m}")
    # print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
    # print(f"Current is_day {current_is_day}")
    # print(f"Current weather_code {current_weather_code}")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(5).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["weather_code"] = hourly_weather_code

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    # print(hourly_dataframe)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        )
    }
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min

    daily_dataframe = pd.DataFrame(data=daily_data)
    # print(daily_dataframe)

    temp = (
        "*The current* **temp** *is* "
        + "```diff\n"
        + "+"
        + current_temperature_2m
        + "°F\n"
        + "```"
    )
    humidity = (
        " *and the* **humidity** *is* "
        + "```diff\n"
        + "+"
        + current_relative_humidity_2m
        + "%\n"
        + "```"
    )
    weather = (
        "*The* **weather** *is* "
        + "```diff\n"
        + "+"
        + weather_codes[current_weather_code]
        + "\n"
        + "```"
    )
    return temp + humidity + weather
