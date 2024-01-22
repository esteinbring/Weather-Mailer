import logging
import openmeteo_requests
import pandas as pd
import requests_cache

from retry_requests import retry


def get_weather_forecast(latitude, longitude, timezone, days):

    logging.info(f"Trying to fetch weather data for the next {days} days for the coordinates {latitude}°E {longitude}°N from Open-Meteo...")

    # Setup the Open-Meteo API client
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # See openmeteo's documentation https://open-meteo.com/en/docs before making changes!
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_probability_max', 'wind_speed_10m_max'],
        'timezone': timezone, 
        'forecast_days': days + 2 # Add 2 days because open meteo is 2 days behind
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process data. The order of variables needs to be the same as requested.
    weather_data = responses[0].Daily()

    daily_temperature_2m_max = weather_data.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = weather_data.Variables(1).ValuesAsNumpy()
    daily_precipitation_probability_max = weather_data.Variables(2).ValuesAsNumpy()
    daily_wind_speed_10m_max = weather_data.Variables(3).ValuesAsNumpy()

    datetime = pd.date_range(
        start = pd.to_datetime(weather_data.Time(), unit = 's'),
        end = pd.to_datetime(weather_data.TimeEnd(), unit = 's'),
        freq = pd.Timedelta(seconds = weather_data.Interval()),
        inclusive = 'left'
    )

    weather = {
        'Date': datetime.date,
        'Weekday': datetime.day_name(),
        'Temperature (min) in °C' : daily_temperature_2m_min.astype(int),
        'Temperature (max) in °C': daily_temperature_2m_max.astype(int),
        'Precipitation probability in %' : daily_precipitation_probability_max,
        'Wind speed in km/h': daily_wind_speed_10m_max.astype(int)
    }

    weather_dataframe = pd.DataFrame(data = weather)

    # It's hard to predict precipitation for 7+ days so sometimes there is no data
    weather_dataframe['Precipitation probability in %'] = weather_dataframe['Precipitation probability in %'].astype('Int64')

    # Remove the first two days (which lie in the past)
    weather_dataframe = weather_dataframe.iloc[2:] 

    logging.info(f"Successfully fetched and processed the weather data \
                 for the next {days} days for the coordinates {latitude}°E {longitude}°N.")

    return weather_dataframe

