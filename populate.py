import csv
import os
import urllib,threading

import pandas as pd

from tracking_board_project.settings import STATIC_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracking_board_project.settings')

import django

django.setup()

from tracker.crawler import store_detail_data,store_country_data


def populate():
    thread = threading.Thread(target=store_country_data())
    thread.start()
    thread.join()
    store_detail_data(300)

def fetchdata(url):
    response = urllib.request.urlopen(url)
    decode_data = response.read()
    print(decode_data)
    # file_path = os.path.join(STATIC_DIR, 'temp_files/data.csv')
    #
    # with open(file_path, 'w') as csvfile:
    #     writer = csv.writer(csvfile, lineterminator='\n')

if __name__ == '__main__':
    print('Starting Population Script...')
    populate()
    print('Completed!')

    # url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/02-22-2020.csv"
    # c = pd.read_csv(url, error_bad_lines=False)
    # print(c)
    # fetchdata(url)