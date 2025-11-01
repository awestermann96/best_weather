import requests
import json
import pandas as pd
import datetime as dt
import numpy as np

API_key = '27da32eb-30c9-4f67-8010-ce06e2fa6dbe'

time_periods = [dt.time(n) for n in [0, 3, 6, 9, 12, 15, 18, 21]]

met_dp = 'http://datapoint.metoffice.gov.uk/public/data/'

sites_url = 'val/wxfcs/all/json/sitelist'

sites = requests.get(met_dp + sites_url + '?key=' + API_key)

sites_json = sites.json().get('Locations').get('Location')

sites_df = pd.DataFrame(sites_json)
sites_df = sites_df.drop(['elevation', 'id', 'obsSource'], axis=1)
sites_df = sites_df.sort_values('region')

regions = sites_df['region'].unique()

regions_dict = {'nw': 'North West', 'os': 'Orkney & Shetland', 
                'gr': 'Grampian', 'he': 'Highlands & Eilean Siar',
                'ni': 'Northern Ireland', 'se': 'London & South East',
                'ee': 'East', 'wm': 'West Midlands',
                'wl': 'Wales', 'dg': 'Dumfries, Galloway, Lothian & Borders', 
                'st': 'Strathclyde', 'ne': 'North East',
                'yh': 'Yorkshire & Humber', 'em': 'East Midlands',
                'sw': 'South West', 'ta': 'Central, Tayside & Fife'}

sites_df['region'] = sites_df['region'].map(regions_dict)

sites_df.to_csv('Sites_List.csv', index=False)


#####################

sites_region = {item.get('id'): item.get('region') for item in sites_json}



forecast_url = 'val/wxfcs/all/json/all?res=3hourly'

forecast = requests.get(met_dp + forecast_url + '&key=' + API_key)

big_json = forecast.json()

data_list = big_json.get('SiteRep').get('DV').get('Location')

### loop through locations, days and hours to create dataset

df = pd.DataFrame()

for n, location in enumerate(data_list):

    forecasts = location.get('Period')

    df_day = pd.DataFrame()

    for day in forecasts:

        hourly = day.get('Rep')

        df_hour = pd.DataFrame()

        for hour in hourly:
            df_hour = pd.concat([df_hour, pd.json_normalize(hour)])

        date = day.get('value')

        df_hour['date'] = dt.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))

        df_day = pd.concat([df_day, df_hour])

    # add area metadata - don't need elevation?
    meta = {k:v for k, v in location.items() if k in ['i', 'lat', 'lon', 'name']}

    for name in meta.keys():
        df_day[name] = meta[name]
    
    df = pd.concat([df, df_day])

    print(n)

# metadata and recoding
df['region'] = df['i'].map(sites_region)

df['time'] = (df['$'].astype(int) / 60).astype(int)

params_list = big_json.get('SiteRep').get('Wx').get('Param')

params_dict = {'F': 'feels_temp', 'G': 'wind_gust', 'H': 'humidity',
               'T': 'temp', 'V':'visibility', 'D': 'wind_dir',
               'S': 'wind_speed', 'U': 'max_UV', 'W':'weather_type',
               'Pp':'rain_prob'}

df['weather_type'] = df['weather_type'].astype(int)

df['rain'] = np.where(df['weather_type'] >= 9, 1, 0)

df['rain2'] = np.where(df['rain_prob'].astype(int) >= 50, 1, 0)