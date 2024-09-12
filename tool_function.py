import requests
import streamlit as st
import json
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("Weahter API Key:",OPEN_WEATHER_API_KEY)

df = pd.read_csv('country_code.csv', header = 0)
df['name'] = df['name'].str.upper()

def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print("Error:", response.status_code)
    return data

def get_geo_data_from_city_or_zip(zip_code=None, country_name=None, city_name=None,):
    '''Get Geographical data with latitude and longitude using zip code and country name or city name and country name combinations. When zip code is passed, country name must be present.'''
    try:
        country_code = None
        if country_name is not None:
            country_code = (df[(df['name'] == country_name.upper()) | (df['alpha-2'] == country_name.upper()) | (df['alpha-3'] == country_name.upper())]['alpha-2']).iloc[0]
        if city_name is None and zip_code is None:
            return "Need city name or zip code"
        if zip_code is not None:
            # url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key.OPEN_WEATHER_API_KEY}'
            url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={OPEN_WEATHER_API_KEY}'
            geo_data = get_response(url)
        elif city_name is not None:
            url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={OPEN_WEATHER_API_KEY}'
            url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={OPEN_WEATHER_API_KEY}'
            geo_data = get_response(url)[0]
        else:
            return "Wrong"
        return geo_data
    except:
        return "Something is wrong in get geo data tool. There is a chance that zipcode is given without country name. Get that from the user."


def get_weather(geo_data, is_forecast, local_requested_timestamp):
    '''Getting current weather or forecast for the upcoming 5 days (not more than that) at a specified geo location. Geo data must be received from get_geo_data_from_city_or_zip before calling this tool. If it's a forecast, we MUST need the local_requested_timestamp generated from get_local_datetime tool.'''

    try:
        if not is_forecast:
            # url = f'https://api.openweathermap.org/data/2.5/weather?lat={geo_data['lat']}&lon={geo_data['lon']}&appid={api_key.OPEN_WEATHER_API_KEY}&units=imperial'
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={geo_data['lat']}&lon={geo_data['lon']}&appid={OPEN_WEATHER_API_KEY}&units=imperial"
            data = get_response(url)
            return data
        else:
            # url = f'https://api.openweathermap.org/data/2.5/forecast?lat={geo_data['lat']}&lon={geo_data['lon']}&appid={api_key.OPEN_WEATHER_API_KEY}&units=imperial'
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={geo_data['lat']}&lon={geo_data['lon']}&appid={OPEN_WEATHER_API_KEY}&units=imperial"
            data = get_response(url)
            only_date_json = {}
            value = data["list"][0]["dt"]
            for i in data["list"]:
                if abs(i["dt"] - local_requested_timestamp) > value:
                    break
                else:
                    value = abs(i["dt"] - local_requested_timestamp)
                    only_date_json = i
                    print(value)
            
            return only_date_json
    except:
        return "Tool has been called in the wrong order. Call get_geo_data_from_city_or_zip with relevant parameters first."

def get_local_datetime(geo_data, days = 0, hour = 10):
    '''If a future weather forecast is queried, this tool must be called and the returned value MUST be used in get_weather function's local_requested_timestamp variable.'''
    from datetime import datetime, timedelta
    from timezonefinder import TimezoneFinder
    import pytz
    obj = TimezoneFinder()
    latitude =  geo_data["lat"]
    longitude = geo_data["lon"]
    local_timezone= obj.timezone_at(lng=longitude, lat=latitude)
    local_requested_datetime = (datetime.now(pytz.timezone(local_timezone)) + timedelta(days = days))
    if days != 0:
        local_requested_datetime = local_requested_datetime.replace(hour=hour, minute=0, second=0)
    return local_requested_datetime.timestamp()
