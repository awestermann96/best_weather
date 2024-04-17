import requests
import json

API_key = '27da32eb-30c9-4f67-8010-ce06e2fa6dbe'

met_dp = 'http://datapoint.metoffice.gov.uk/public/data/'

sites_url = 'val/wxfcs/all/json/sitelist'

sites = requests.get(met_dp + sites_url + '?key=' + API_key)

sites_json = sites.json().get('Locations').get('Location')

sites_list = [dicty.get('name') for dicty in sites_json]

sites_dict = {item.get('name'): item.get('id') for item in sites_json}

sites.status_code

#####################

forecast_url = 'val/wxfcs/all/json/3840?res=3hourly'

forecast = requests.get(met_dp + forecast_url + '?key=' + API_key)