
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

from weatherapp.models import WeatherData

from math import ceil
import time

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"

# set up main data frame
df = pd.DataFrame()

# read in sites data we want weather for
sites_lookup = pd.read_csv('Sites_List.csv')

# do responses in batches of 500
n_batches = ceil(len(sites_lookup) / 100)

for n in range(0, n_batches):

    # get start and end index of batch to include in response
    start = n * 100 
    end = (n + 1) * 100 - 1

    params = {
        "latitude": sites_lookup.loc[start: end, 'latitude'].to_list(),
        "longitude": sites_lookup.loc[start: end, 'longitude'].to_list(),
        "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "weather_code", "cloud_cover", "wind_speed_10m"]
    }
    
    # Only allows certain number of requests per minute
    try:
        responses = openmeteo.weather_api(url, params=params)
        print(n)
    except:
        print('timed out')
        time.sleep(65)
        responses = openmeteo.weather_api(url, params=params)
        print(n)

    # iterate through all sites
    for site_no in range(0, len(responses)):
        response = responses[site_no]

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(4).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["apparent_temperature"] = hourly_apparent_temperature
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

        site_df = pd.DataFrame(data = hourly_data)
        site_df['latitude'] = response.Latitude()
        site_df['longitude'] = response.Longitude()
        site_df['Site'] = sites_lookup.loc[start: end, 'name'].to_list()[site_no]
        
        df = pd.concat([df, site_df])

# condense data to every 4 hours
df['DayName'] = df['date'].dt.day_name()
df['Hour'] = df['date'].dt.hour

hour_periods = 4 * ['12am - 4am'] + 4 * ['4am - 8am'] + 4 * ['8am - 12pm'] + \
            4 * ['12pm - 4pm'] + 4 * ['4pm - 8pm'] + 4 * ['8pm - 12am']

df['Period'] = df['Hour'].map(dict(zip(range(0, 24), hour_periods)))

# More efficient to store number rather than date
df['Date'] = df['date'].dt.day
df['Month'] = df['date'].dt.month

weather_codes = df[['longitude', 'latitude', 'Date', 'Period', 'weather_code']]

# average over 4 hours
df_agg = df.groupby(['longitude','latitude','Date','DayName','Site','Month','Period']).\
    agg({'temperature_2m': 'mean',
         'apparent_temperature': 'mean',
         'precipitation_probability': 'mean',
         'cloud_cover': 'mean',
         'wind_speed_10m': 'mean'}).reset_index()

df_join = df_agg.merge(sites_lookup, how = 'left', left_on = 'Site', right_on = 'name')

df_score = df_join.rename(columns = {'longitude_x': 'longitude',
                                     'latitude_x': 'latitude'})

# weather score calculation
def weather_score(temp, rain):
    return temp * ((100 - rain) / 100)

df_score['weather_score'] = df_join.apply(lambda x: weather_score(x['apparent_temperature'],
                                            x['precipitation_probability']),
                                            axis=1)

df_score.to_csv('Weather_Data.csv', index = False)

