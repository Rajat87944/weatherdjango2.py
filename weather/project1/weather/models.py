from django.db import models

# Create your models here.

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    coordinate = models.CharField(max_length=50)
    temperature = models.FloatField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    main = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.main} ({self.timestamp})"