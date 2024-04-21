import requests
import json
import pandas as pd
import datetime as dt

API_key = '27da32eb-30c9-4f67-8010-ce06e2fa6dbe'

time_periods = [dt.time(n) for n in [0, 3, 6, 9, 12, 15, 18, 21]]

met_dp = 'http://datapoint.metoffice.gov.uk/public/data/'

sites_url = 'val/wxfcs/all/json/sitelist'

sites = requests.get(met_dp + sites_url + '?key=' + API_key)

sites_json = sites.json().get('Locations').get('Location')

sites_list = [dicty.get('name') for dicty in sites_json]

sites_dict = {item.get('name'): item.get('id') for item in sites_json}

sites.status_code

# get time periods available
tps_url = 'val/wxfcs/all/json/capabilities?res=3hourly'
tps = requests.get(met_dp + tps_url + '&key=' + API_key).json().get('Resource').get('TimeSteps').get('TS')

#####################

forecast_url = 'val/wxfcs/all/json/all?res=3hourly'

forecast = requests.get(met_dp + forecast_url + '&key=' + API_key)

big_json = forecast.json()

params_list = big_json.get('SiteRep').get('Wx').get('Param')

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

        df_hour['time_period'] = time_periods[:len(df_hour)]

        date = day.get('value')

        df_hour['date'] = dt.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))

        df_day = pd.concat([df_day, df_hour])

    # add area metadata - don't need elevation?
    meta = {k:v for k, v in location.items() if k in ['i', 'lat', 'lon', 'name']}

    for name in meta.keys():
        df_day[name] = meta[name]
    
    df = pd.concat([df, df_day])

    print(n)

#df['region'] = df['id'].map()
