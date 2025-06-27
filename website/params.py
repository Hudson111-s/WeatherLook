CURRENT_PARAMS = ["temperature_2m","relative_humidity_2m",
                  "apparent_temperature","precipitation",
                  "rain","showers","snowfall",
                  "cloud_cover","pressure_msl","surface_pressure",
                  "wind_speed_10m","wind_direction_10m","wind_gusts_10m"]

DAILY_PARAMS = ["temperature_2m_max","temperature_2m_min",
                "dew_point_2m_max", "dew_point_2m_min",
                "apparent_temperature_max", "apparent_temperature_min",
                "uv_index_max", "uv_index_clear_sky_max",
                "precipitation_sum", "rain_sum",
                "snowfall_sum", "precipitation_hours",
                "precipitation_probability_max", "wind_speed_10m_max",
                "wind_gusts_10m_max", "wind_direction_10m_dominant",
                "shortwave_radiation_sum", "et0_fao_evapotranspiration"]

UNITS_PARAMS = {"&temperature_unit=fahrenheit", "&wind_speed_unit=ms",
                "&wind_speed_unit=mph","&wind_speed_unit=kn",
                "&precipitation_unit=inch"}

CURRENT_PARAMS_READABLE = {
    "temperature_2m": "Temperature (2m)",
    "relative_humidity_2m": "Relative Humidity (2m)",
    "apparent_temperature": "Apparent Temperature",
    "precipitation": "Total Precipitation",
    "rain": "Total Rainfall",
    "showers": "Showers",
    "snowfall": "Total Snowfall",
    "cloud_cover": "Cloud Cover",
    "pressure_msl": "Sealevel Pressure",
    "surface_pressure": "Surface Pressure",
    "wind_speed_10m": "Wind Speed (10m)",
    "wind_direction_10m": "Wind Direction (10m)",
    "wind_gusts_10m": "Wind Gusts (10m)"}

DAILY_PARAMS_READABLE = {
    "temperature_2m_max": "Max Temperature (2m)",
    "temperature_2m_min": "Min Temperature (2m)",
    "dew_point_2m_max": "Max Dewpoint (2m)",
    "dew_point_2m_min": "Min Dewpoint (2m)",
    "apparent_temperature_max": "Max Apparent Temperature",
    "apparent_temperature_min": "Min Apparent Temperature",
    "uv_index_max": "Max UV Index",
    "uv_index_clear_sky_max": "Max UV Index (Clear Sky)",
    "precipitation_sum": "Total Precipitation",
    "rain_sum": "Total Rainfall",
    "snowfall_sum": "Total Snowfall",
    "precipitation_hours": "Precipitation Hours",
    "precipitation_probability_max": "Precipitation Probability",
    "wind_speed_10m_max": "Max Wind Speed (10m)",
    "wind_gusts_10m_max": "Max Wind Gusts (10m)",
    "wind_direction_10m_dominant": "Wind Direction (10m)",
    "shortwave_radiation_sum": "Total Shortwave Radiation",
    "et0_fao_evapotranspiration":"Reference Evapotranspiration"}
