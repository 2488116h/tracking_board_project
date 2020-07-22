import csv
import json
import os
import threading
import time
import datetime
import urllib.request
from django.db.models import Sum, F

from django.core.paginator import Paginator
from django.shortcuts import render
from tracker.crawler import task
from tracker.models import Country, Detail_Data_country

from tracking_board_project.settings import STATIC_DIR

from django.http import JsonResponse


def index(request):
    # task()
    dataset = {}
    # data = Country.objects.all()
    world = Country.objects.get(country_code='OWID_WRL')
    world_data = Detail_Data_country.objects.get(country=world, date=datetime.date.today() - datetime.timedelta(days=1))
    query = Detail_Data_country.objects.exclude(country=world).filter(
        date=datetime.date.today() - datetime.timedelta(days=1))
    data = query.order_by('-total_cases')[:10]
    detail_data = query.order_by('-total_cases')
    # paginator = Paginator(dataset, 10)
    # detail_data = paginator.page(1)
    # chart()
    dataset['Top10_Data'] = data
    dataset['Detail'] = detail_data
    dataset['WorldData'] = world_data

    return render(request, 'tracker/index.html', context=dataset)


def chart(request):
    data = {}
    q = Detail_Data_country.objects.filter(date=datetime.date.today() - datetime.timedelta(days=1)).exclude(
        country_id='OWID_WRL')
    query = q.values('country__continent').annotate(name=F('country__continent')).annotate(value=Sum('total_cases'))

    print(query.query.__str__())
    data['data_pie'] = list(query)

    return JsonResponse(data)


def country(request):
    data = {}
    query = Detail_Data_country.objects.filter(country_id=request.GET.get('country_id'))
    data['Data'] = query
    return render(request, 'tracker/country.html', context=data)
