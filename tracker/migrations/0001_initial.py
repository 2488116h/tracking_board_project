# Generated by Django 2.1.5 on 2020-09-05 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_name', models.CharField(max_length=128)),
                ('country_code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('country_2digits_code', models.SlugField(default='ts', max_length=3)),
                ('continent', models.CharField(max_length=128)),
                ('population', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True)),
                ('population_density', models.DecimalField(decimal_places=3, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Detail_Data_country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cases', models.DecimalField(decimal_places=0, max_digits=20)),
                ('total_cases', models.DecimalField(decimal_places=0, max_digits=20)),
                ('cases_per_million', models.DecimalField(decimal_places=3, max_digits=20)),
                ('total_cases_per_million', models.DecimalField(decimal_places=3, max_digits=20)),
                ('deaths', models.DecimalField(decimal_places=0, max_digits=20)),
                ('total_deaths', models.DecimalField(decimal_places=0, max_digits=20)),
                ('deaths_per_million', models.DecimalField(decimal_places=3, max_digits=20)),
                ('total_deaths_per_million', models.DecimalField(decimal_places=3, max_digits=20)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Country')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='detail_data_country',
            unique_together={('date', 'country')},
        ),
    ]
