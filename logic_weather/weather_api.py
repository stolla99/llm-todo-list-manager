from typing import Any

import requests
from pyowm import OWM

open_weather_map_api_token = '<place api token here>'


def fetch_geocode(city_name, country_code, limit):
    """
    This function fetches the geocode (latitude and longitude) for a given city using the OpenWeatherMap API.

    Args:
        city_name (str): The name of the city.
        country_code (str): The country code of the city.
        limit (int): The maximum number of locations to retrieve.

    Returns:
        tuple: A tuple containing the latitude and longitude of the city.
    """
    owm = OWM(open_weather_map_api_token)
    mgr = owm.geocoding_manager()
    list_of_locations = mgr.geocode(city_name, country=country_code, limit=limit)
    city = list_of_locations[0]
    city_lat = city.lat
    city_lon = city.lon
    return city_lat, city_lon


def fetch_weather_forecast(lon: Any, lat: Any, country_code="DE"):
    """
    This function fetches the weather forecast for a given location using the OpenWeatherMap API.

    Args:
        lon (float): The longitude of the location.
        lat (float): The latitude of the location.
        country_code (str, optional): The country code of the location. Defaults to "DE".

    Returns:
        tuple: A tuple containing the status code of the response and the weather forecast data.
               If the status code is 200, the weather forecast data is a dictionary that contains a list of weather forecasts.
               Each forecast is a dictionary that contains the date and time of the forecast ('dt_txt'),
               the temperature ('main' -> 'temp'), and the description of the weather ('weather' -> 'description').
               If the status code is not 200, the weather forecast data is the response text.
    """
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    parameters = {
        'lat': lat,
        'lon': lon,
        'appid': open_weather_map_api_token,
        'units': 'metric'
    }
    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        weather_forecast_data = response.json()
        return response.status_code, weather_forecast_data
    else:
        return response.status_code, response.text


def get_weather_string(weather_forecast_data) -> str:
    """
    This function formats the weather forecast data into a string.

    Args:
        weather_forecast_data (dict): The weather forecast data. The data is a dictionary that contains a list of weather forecasts.
                                     Each forecast is a dictionary that contains the date and time of the forecast ('dt_txt'),
                                     the temperature ('main' -> 'temp'), and the description of the weather ('weather' -> 'description').

    Returns:
        str: A string containing the weather forecast. Each forecast is represented as a string in the format:
             "{datetime}: {temp}°C, {description}". The forecasts are separated by newlines.
    """
    filtered_five_day_forecast = [
        {
            'datetime': step['dt_txt'],
            'temp': step['main']['temp'],
            'description': step['weather'][0]['description']
        } for step in weather_forecast_data['list']
    ]
    forecast_str = "\n".join(
        [
            f"{step['datetime']}: {step['temp']}°C, {step['description']}" for step in filtered_five_day_forecast
        ]
    )
    return forecast_str
