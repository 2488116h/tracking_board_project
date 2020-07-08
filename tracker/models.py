from django.db import models


# Create your models here.
class Data(models.Model):
    date = models.DateField(blank=False)
    country = models.CharField(max_length=128, blank=False)
    country_code = models.CharField(max_length=2)
    region = models.CharField(max_length=128)
    population = models.IntegerField(blank=True, null=True)
    cases = models.IntegerField()
    deaths = models.IntegerField()

    def __str__(self):
        return self.name
