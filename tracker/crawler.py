import csv
import os
import ssl
import threading
import time, datetime
from decimal import Decimal
import pandas as pd
from urllib.request import urlretrieve

from tracking_board_project.settings import STATIC_DIR

from tracker.models import Country, Detail_Data_country

ssl._create_default_https_context = ssl._create_unverified_context


def task():
    print('Task Start... ')
    detail_data = threading.Thread(target=get_detail_data('https://covid.ourworldindata.org/data/owid-covid-data.csv'))
    detail_data.start()
    detail_data.join()
    store_detail_data(2)


def get_detail_data(url):
    """
    Fetch the daily data from the api
    :param url: address of daily data
    :return:
    """
    print('Fetching Data...')
    file_path = os.path.join(STATIC_DIR, 'temp_files/detail.csv')
    try:
        urlretrieve(url, file_path)
    except:
        fetch_daily_data()
        return True
    return False


def fetch_daily_data():
    """
    To use pandas read data and output to csv file
    The method is a backup plan in case failing to download data directly
    :return:
    """
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    c = pd.read_csv(url)
    c.to_csv(os.path.join(STATIC_DIR, 'temp_files/detail.csv'), index=False)


def store_detail_data(days):
    """
    To store daily data into the database
    :param days: update the particular days' date
    :return:
    """
    file_path = os.path.join(STATIC_DIR, 'temp_files/detail.csv')
    with open(file_path, 'r') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)

        for item in reader:

            if not item[0]:
                continue

            date_format = datetime.datetime.strptime(item[3], '%Y-%m-%d')
            if date_format.date() < datetime.date.today() - datetime.timedelta(days=days) or item[4] == '':
                continue

            country_code = Country.objects.get(country_code=item[0])
            try:

                _created = Detail_Data_country.objects.update_or_create(
                    date=date_format, country=country_code,
                    defaults={
                        'total_cases': Decimal(item[4]),
                        'cases': Decimal(item[5]),
                        'total_deaths': Decimal(item[7]),
                        'deaths': Decimal(item[8]),
                        'total_cases_per_million': Decimal(item[10]),
                        'cases_per_million': Decimal(item[11]),
                        'total_deaths_per_million': Decimal(item[13]),
                        'deaths_per_million': Decimal(item[14]),
                    },
                )
            except Exception:
                print(item[0] + item[3] + ' updated failed')
            print(item[0] + item[3] + 'done')
        print('Finished!' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
