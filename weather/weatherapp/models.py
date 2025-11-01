from django.db import models

# when ready, python manage.py migrate 
# also import in admin file

# Create your models here.
class WeatherData(models.Model):
    Site = models.CharField(max_length = 300)
    Area = models.CharField(max_length = 300)
    Region = models.CharField(max_length = 200)
    NationalPark = models.CharField(max_length = 200)
    Time = models.CharField(max_length = 20)
    Date = models.IntegerField()
    Day = models.CharField(max_length = 20)
    Temperature = models.FloatField()
    WeatherScore = models.FloatField()