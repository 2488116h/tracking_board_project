import csv
import json
import os
import threading
import time
import urllib.request

from django.core.paginator import Paginator
from django.shortcuts import render
from tracker.models import Data
from tracking_board_project.settings import STATIC_DIR


def index(request):
    dataset = Data.objects.order_by('-date')
    paginator = Paginator(dataset, 20)
    data = paginator.page(1)

    return render(request, 'tracker/index.html', {'Data': data})


# data crawler crontab
def time_task():
    domain = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
    thread = threading.Thread(target=get_data(domain))
    thread.start()
    thread.join()
    load_data()


def get_data(url):
    response = urllib.request.urlopen(url)
    decode_data = json.loads(response.read())
    file_path = os.path.join(STATIC_DIR, 'temp_files/tests.csv')

    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')

        for item in decode_data['records']:
            item_date = item['dateRep']
            item_cases = item['cases']
            item_deaths = item['deaths']
            item_country = item['countriesAndTerritories']
            item_country_code = item['geoId']
            item_population = item['popData2019']
            item_region = item['continentExp']
            writer.writerow(
                [item_date, item_country, item_country_code, item_region, item_population, item_cases, item_deaths])
        csvfile.close()


def load_data():
    file_path = os.path.join(STATIC_DIR, 'temp_files/tests.csv')
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            test = time.strptime(item[0], '%d/%m/%Y')

            if item[4] == '':
                _, created = Data.objects.get_or_create(
                    date=time.strftime('%Y-%m-%d', test),
                    country=item[1],
                    country_code=item[2],
                    region=item[3],
                    cases=item[5],
                    deaths=item[6]
                )

            else:
                _, created = Data.objects.get_or_create(
                    date=time.strftime('%Y-%m-%d', test),
                    country=item[1],
                    country_code=item[2],
                    region=item[3],
                    population=item[4],
                    cases=item[5],
                    deaths=item[6]
                )
