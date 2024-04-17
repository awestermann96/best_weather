import requests
import json

import urllib.request

API_key = '27da32eb-30c9-4f67-8010-ce06e2fa6dbe'

url = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/3840?res=3hourly'

res = requests.get(url + '&key=' + API_key)

json1 = res.json()

json2 = json1.get('SiteRep')

json3 = json2.get('Wx').get('Param')

json4 = json2.get('DV')

json5 = json4.get('Location')

json6 = json5.get('Period')


