import csv
import json
import os
import ssl
import socket
import threading
import time, datetime
from decimal import Decimal
import urllib
from urllib.request import urlretrieve

from tracking_board_project.settings import STATIC_DIR

from tracker.models import Country, Detail_Data_country

ssl._create_default_https_context = ssl._create_unverified_context


def task():
    # domain = 'https://covid.ourworldindata.org/data/owid-covid-data.json'
    # thread = threading.Thread(target=get_country_data(domain))
    # thread.start()
    # thread.join()
    # store_country_data()
    detail_data = threading.Thread(target=get_detail_data('https://covid.ourworldindata.org/data/owid-covid-data.csv'))
    detail_data.start()
    detail_data.join()
    store_detail_data()


def get_country_data(url):
    response = urllib.request.urlopen(url)
    decode_data = json.loads(response.read())
    file_path = os.path.join(STATIC_DIR, 'temp_files/country.csv')

    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')

        for item in decode_data:
            code = item
            continent = None
            try:
                continent = decode_data[item]['continent']
            except KeyError:
                print('world data')
            country = decode_data[item]['location']
            population = decode_data[item]['population']
            population_density = 0
            try:
                population_density = decode_data[item]['population_density']
            except KeyError:
                print('There is no population density for ' + country)

            cvd_death_rate = 0
            try:
                cvd_death_rate = decode_data[item]['cvd_death_rate']
            except KeyError:
                print('There is no covid death rate for ' + country)

            writer.writerow([code, continent, country, population, population_density, cvd_death_rate])
        print('Country data download finished!')
        csvfile.close()


def store_country_data():
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
                    'cvd_death_rate': item[5]
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


def get_detail_data(url):

    file_path = os.path.join(STATIC_DIR, 'temp_files/detail.csv')
    try:
        urlretrieve(url, file_path)
    except:
        get_detail_data(url)


def store_detail_data():
    file_path = os.path.join(STATIC_DIR, 'temp_files/detail.csv')
    with open(file_path, 'r') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)

        for item in reader:

            if not item[0]:
                continue

            date_format = datetime.datetime.strptime(item[3], '%Y-%m-%d')
            if date_format.date() < datetime.date.today() - datetime.timedelta(days=4) or item[4] == '':
                continue

            country_code = Country.objects.get(country_code=item[0])

            _created = Detail_Data_country.objects.update_or_create(
                date=date_format, country=country_code,
                defaults={
                    'total_cases': Decimal(item[4]),
                    'cases': Decimal(item[5]),
                    'total_deaths': Decimal(item[6]),
                    'deaths': Decimal(item[7]),
                    'total_cases_per_million': Decimal(item[8]),
                    'cases_per_million': Decimal(item[9]),
                    'total_deaths_per_million': Decimal(item[10]),
                    'deaths_per_million': Decimal(item[11]),
                },
            )
            print(item[0] + item[3] + 'done')
        print('Finished!' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# if __name__ == '__main__':
#     task()
