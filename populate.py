import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracking_board_project.settings')
import django

django.setup()

import threading
import csv
from tracker.models import Country
from tracking_board_project.settings import STATIC_DIR
from tracker.crawler import store_detail_data,get_detail_data


def populate():
    """
    Initial basic data : country data from static files and
    latest daily data

    """
    thread = threading.Thread(target=store_country_data())
    thread.start()
    thread.join()

    detail_data = threading.Thread(target=get_detail_data('https://covid.ourworldindata.org/data/owid-covid-data.csv'))
    detail_data.start()
    detail_data.join()
    # store detail data of recent 400 days
    store_detail_data(400)


def store_country_data():
    """
    Insert country data into database

    """
    file_path = os.path.join(STATIC_DIR, 'temp_files/country.csv')
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            _created = Country.objects.update_or_create(
                country_code=item[0],
                defaults={
                    'country_name': item[2],
                    'continent': item[1],
                    'population': item[3],
                    'population_density': item[4],
                }
            )
    with open(os.path.join(STATIC_DIR, 'temp_files/country_codes.csv')) as f:
        r = csv.reader(f)
        for data in r:
            try:
                c = Country.objects.get(country_code=data[0])
                c.country_2digits_code = data[1]
                c.save()
            except Exception:
                print('Not match')

    print('Country data is updated!')


if __name__ == '__main__':
    print('Starting Population Script...')
    populate()
    print('Completed!')
