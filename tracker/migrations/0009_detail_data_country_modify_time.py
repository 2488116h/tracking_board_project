# Generated by Django 2.1.5 on 2020-08-17 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_country_country_2digits_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail_data_country',
            name='modify_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
