import pandas as pd
from weatherapp.models import WeatherData

df = pd.read_csv('Weather_Data.csv')

# update model
def update_database(model, site, area, region, npark, time, date, day, temp, score):
      model.objects.update_or_create(
            Site = site,
            Area = area, 
            Region = region,
            NationalPark = npark,
            Time = time, 
            Date = date, 
            Day = day,
            defaults = {'Temperature': temp,
                        'WeatherScore': score}
      )

df.apply(lambda x: update_database(WeatherData,
                                         x['Site'],
                                         x['unitaryAuthArea'],
                                         x['region'],
                                         x['nationalPark'],
                                         x['Period'],
                                         x['Date'],
                                         x['DayName'],
                                         x['apparent_temperature'],
                                         x['weather_score']),
                                         axis = 1)
