from django.db import models


# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=128, blank=False)
    country_code = models.CharField(max_length=10, unique=True, primary_key=True)
    continent = models.CharField(max_length=128)
    population = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=0)
    population_density = models.DecimalField(max_digits=20, decimal_places=3)
    cvd_death_rate = models.DecimalField(max_digits=20, decimal_places=3)

    def __str__(self):
        return self.country_code


class Detail_Data_country(models.Model):
    date = models.DateField(blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    cases = models.DecimalField(max_digits=20, decimal_places=0)
    total_cases = models.DecimalField(max_digits=20, decimal_places=0)
    cases_per_million = models.DecimalField(max_digits=20, decimal_places=3)
    total_cases_per_million = models.DecimalField(max_digits=20, decimal_places=3)
    deaths = models.DecimalField(max_digits=20, decimal_places=0)
    total_deaths = models.DecimalField(max_digits=20, decimal_places=0)
    deaths_per_million = models.DecimalField(max_digits=20, decimal_places=3)
    total_deaths_per_million = models.DecimalField(max_digits=20, decimal_places=3)

    class Meta:
        unique_together = ('date', 'country')

    # def __str__(self):
    #     return self.country.
