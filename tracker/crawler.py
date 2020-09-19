import csv
import json
import os
import ssl
import logging
import socket
import threading
import time, datetime
from decimal import Decimal
import urllib
import pandas as pd
import requests
from requests.exceptions import ConnectionError
from urllib.request import urlretrieve

from tracking_board_project.settings import STATIC_DIR

from tracker.models import Country, Detail_Data_country

ssl._create_default_https_context = ssl._create_unverified_context

URL1 = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
URL2 = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'


def task():
    logging.info('Task Start... ')
    session = requests.Session()
    urls = [URL1, URL2]
    file_path = os.path.join(STATIC_DIR, 'temp_files/detail.csv')
    detail_data = threading.Thread(target=get_detail_data, args=(session, urls, file_path))
    detail_data.start()
    detail_data.join()
    store_detail_data(2)


def get_detail_data(session, urls, filepath):
    """
    Fetch the daily data from the api
    :param url: address of daily data
    :return:
    """
    for url in urls:
        try:
            resp = session.get(url, timeout=5)
        except ConnectionError:
            print("Failed to get from {}".format(url))
            continue
        else:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            return True
    return False


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
    return True
