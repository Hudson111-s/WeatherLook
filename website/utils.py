from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from logging import getLogger, INFO, Formatter, Logger
from logging.handlers import RotatingFileHandler
from re import compile, Pattern
from io import StringIO 
from csv import writer
import os
from datetime import datetime
from website.params import *

# In-memory cache.
location_cache = {}

#------------------------------------------------------------------------------------------------------------------------------------

def create_geolocator() -> RateLimiter:
    """
    Uses geopy to create Nominatim user_agent.
    
    Returns:
        RateLimiter.    
    """
     
    geolocator = Nominatim(user_agent="WeatherLook", timeout=10)
    rate_limiter = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    return rate_limiter

#------------------------------------------------------------------------------------------------------------------------------------

def get_location_coordinates(location: str, rate_limiter: RateLimiter, logger: Logger):
    """
    Turns location into latitude and longitude.

    :param (str) location: String of location.
    :param rate_limiter: Geopy rate_limiter object.
    :param logger: Logger for error logging.  
    
    Returns:
        Tuple including Location in latitude, longitude and msg if err.
    """

    try:
        cached_location = location_cache.get(location.strip().lower())
        if cached_location:
            return cached_location, None

        location_ll = rate_limiter(location)
        if not location_ll:
            logger.error(f"Failed to geocode location: {location}")
            return None, f"{location} is a invalid location, try another!"
        
        location_cache[location.strip().lower()] = location_ll
        return location_ll, None
    
    except Exception as e:
        logger.exception(f"Something when wrong while getting location coordinates: {e}")
        return None, "Something went wrong, try again later!"

#------------------------------------------------------------------------------------------------------------------------------------

def create_logger() -> Logger:
    """Creates basic logger"""
    logger = getLogger(__name__)
    logger.setLevel(INFO)

    log_path = "logs/weather_look.log"
    os.makedirs("logs", exist_ok=True)

    file_handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=3)
    file_handler.setFormatter(Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(file_handler)

    try:
        os.chmod(log_path, 0o600)
    except PermissionError:
        logger.warning("Could not set log file permissions.")

    return logger

#------------------------------------------------------------------------------------------------------------------------------------

def create_valid_pattern() -> Pattern:
    return compile("^[\\w\\s,.'-]+$")

#------------------------------------------------------------------------------------------------------------------------------------

def stream_csv_from_json (forecast_is_current: bool, weather_params: list[str], weather_json: dict):
    """
    Streams csv file using json based on forecast length

    :param (bool) forecast_is_current: States if the forecast is 'current' or 'daily'.
    :param (list) weather_params: List of weather params for API.
    :param (dict) weather_json: Weather api response in json.
    """
    buffer = StringIO()
    wtr = writer(buffer)

    # Add for Excel compatibility.
    yield '\ufeff'

    if forecast_is_current:

        wtr.writerow(["Weather", "Value"])
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)

        for param in weather_params:
            value = f"{weather_json['current'][param]} {weather_json['current_units'][param]}"
            wtr.writerow([CURRENT_PARAMS_READABLE[param], value])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)
        
    else:

        wtr.writerow(["Weather", "Value", "Date"])
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)
            
        date = weather_json["daily"]["time"]
        for param in weather_params:
            unit = weather_json["daily_units"][param]
            values = weather_json["daily"][param]
    
            for index, data in enumerate(values):
                value = f"{data} {unit}"
                wtr.writerow([DAILY_PARAMS_READABLE[param], value, date[index]])
                yield buffer.getvalue()
                buffer.seek(0)
                buffer.truncate(0)

#------------------------------------------------------------------------------------------------------------------------------------

def validate_input(input_value: str, pattern: Pattern, logger: Logger) -> str | None:
    """
    Validates input against a regex pattern.

    :param (str) input_value: The user input string.
    :param pattern: Regex pattern to validate against.
    :param logger: Logger for error logging.

    Returns:
        None if input is valid, else a err msg.
    """
    if not input_value or not pattern.match(input_value):
        logger.error(f"Invalid input violated regex pattern: {input_value}")
        return f"{input_value} is invalid. Please correct and try again."
    
#------------------------------------------------------------------------------------------------------------------------------------

def validate_date_range(dates: tuple[str, str]) -> str | None:
    """
    :param (tuple) dates: Tuple that has (start date, end date) 

    Returns:
        Error msg if invalid, else None
    """
    try:
        if not dates[0] or not dates[1]:
            raise ValueError("Missing one or more dates.")
        
        start_date = datetime.strptime(dates[0], "%Y-%m-%d")
        end_date = datetime.strptime(dates[1], "%Y-%m-%d")
        today = datetime.today()

        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date.")
        if end_date > today:
            raise ValueError("End date cannot be in the future.")
        if start_date.year < 2020:
            raise ValueError("Start date must be 2020 or later.")
        if (end_date - start_date).days > 62:
            raise ValueError("Date range is limited to 2 months") 

    except ValueError as e:
        return str(e)
    
#------------------------------------------------------------------------------------------------------------------------------------

def validate_url_params(forecast: str, weather_params: list[str], weather_units: list[str]) -> list:
    """
    Validates forecast type, weather params, and units for API URL.
    
    Returns:
        A list of URL components and an err if any.
    """
    if forecast == "&current=":
        forecast_is_current = True
        url_weather_params = [param for param in weather_params if param in CURRENT_PARAMS]
        if not url_weather_params:
            return [None, None, None, None, None, "Please select one or more checkboxes"]
                
        url_forecast = forecast
        url_forecast_length = "" # Default value (7 days).

    else:
        forecast_is_current = False
        url_weather_params = [param for param in weather_params if param in DAILY_PARAMS]
        if not url_weather_params:
           if not url_weather_params:
                return [None, None, None, None, None, "Please select one or more checkboxes"]
            
        url_forecast = "&daily="

        if forecast in {"&forecast_days=1", "&forecast_days=16"}:
            url_forecast_length = forecast
        else:
            url_forecast_length = ""

    url_units = [param for param in weather_units if param in UNITS_PARAMS]

    return [forecast_is_current, url_forecast, url_forecast_length, url_weather_params, url_units, None]
