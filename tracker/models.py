from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=128, blank=False)
    country_code = models.CharField(max_length=10, unique=True, primary_key=True)
    country_2digits_code = models.SlugField(max_length=3, default='ts')
    continent = models.CharField(max_length=128)
    population = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=0)
    population_density = models.DecimalField(max_digits=20, decimal_places=3)
    cvd_death_rate = models.DecimalField(max_digits=20, decimal_places=3)

    def save(self, *args, **kwargs):
        # self.country_code = slugify(self.country_code)
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.country_name



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
    modify_time = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        unique_together = ('date', 'country')

# class Country_Data(models.Model):
#     date = models.DateField(blank=False)
#     country = models.ForeignKey(Country, on_delete=models.CASCADE)
#     cases = models.DecimalField(max_digits=20, decimal_places=0)
#     total_cases = models.DecimalField(max_digits=20, decimal_places=0)
#     cases_per_million = models.DecimalField(max_digits=20, decimal_places=3)
#     total_cases_per_million = models.DecimalField(max_digits=20, decimal_places=3)
#     deaths = models.DecimalField(max_digits=20, decimal_places=0)
#     total_deaths = models.DecimalField(max_digits=20, decimal_places=0)
#     deaths_per_million = models.DecimalField(max_digits=20, decimal_places=3)
#     total_deaths_per_million = models.DecimalField(max_digits=20, decimal_places=3)
#     total_recovery = models.DecimalField(max_digits=20, decimal_places=0)
#     modify_time = models.DateTimeField(auto_now=True, blank=True)
#
# class Detail_Data_Province_State(models.Model):
#     country = models.ForeignKey(Detail_Data_country, on_delete=models.CASCADE)
#     province_state_code = models.CharField(max_length=128, blank=False)
#     province_state_name = models.CharField(max_length=128, blank=False)
#     cases = models.DecimalField(max_digits=20, decimal_places=0)
#     deaths = models.DecimalField(max_digits=20, decimal_places=0)
#     total_cases = models.DecimalField(max_digits=20, decimal_places=0)
#     total_deaths = models.DecimalField(max_digits=20, decimal_places=0)
#     total_recovery = models.DecimalField(max_digits=20, decimal_places=0)
#     modify_time = models.DateTimeField(auto_now=True, blank=True)
