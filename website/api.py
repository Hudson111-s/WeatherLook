import requests
from typing import Any, Dict, Optional, List, Tuple
from flask import current_app

def call_api(api_url: str, timeout: int) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Calls api URL with error handling.

    :param api_url: URL for API.
    :param timeout: Time in seconds until request stops trying to get.

    :return: Tuple of json and msg if err.
    """
    try:
        results = requests.get(api_url, timeout=timeout)
        if results.status_code != 200:
            current_app.logger.error(f"Failed get call to open-meteo: {results.status_code}")
            return None, "Something went wrong, try again later!"
    except requests.RequestException as e:
        current_app.logger.exception(f"Failed to connect to open-meteo: {e}")
        return None, "Unable to connect to weather service."
    
    return results.json(), None


def build_api_url(location_coordinates: Any, url_weather_params: List[str], url_units: List[str], url_forecast: str, url_forecast_length: str) -> str:
    """
    Builds api url.

    :param location_coordinates: Is the location coordinates after it has been check and sanitised.
    :param url_weather_params: List of weather params for API.
    :param url_units: Weather units for API.
    :param url_forecast: The amount of forecast data wanted (daily or current).
    :param url_forecast_length: How many days of forecast data.

    :return: Complete open-meteo API URL.
    """
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={location_coordinates.latitude}&longitude={location_coordinates.longitude}" + url_forecast
    api_url += ",".join(url_weather_params) + "".join(url_units) + url_forecast_length
    return api_url


def build_history_api_url(location_coordinates: Any, url_weather_params: List[str], url_units: List[str], url_dates: Tuple[str, str]) -> str:
    """
    Builds api url.

    :param location_coordinates: Is the location coordinates after it has been check and sanitised.
    :param url_weather_params: List of weather params for API.
    :param url_units: Weather units for API.
    
    :return: A complete Open-Meteo historical forecast API URL.
    """
    api_url = f"https://historical-forecast-api.open-meteo.com/v1/forecast?latitude={location_coordinates.latitude}&longitude={location_coordinates.longitude}&start_date={url_dates[0]}&end_date={url_dates[1]}&daily="
    api_url += ",".join(url_weather_params) + "".join(url_units)
    return api_url
