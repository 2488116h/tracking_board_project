
import datetime
import urllib.request
from django.db.models import Sum, F

from django.core.paginator import Paginator
from django.shortcuts import render

from tracker.models import Country, Detail_Data_country
from tracker.crawler import task

from django.http import JsonResponse


def index(request):
    task()
    dataset = {}
    # data = Country.objects.all()
    world = Country.objects.get(country_code='OWID_WRL')
    world_data = Detail_Data_country.objects.filter(country=world).order_by('-date')[:1]
    query = Detail_Data_country.objects.exclude(country=world).filter(
        date=datetime.date.today())
    if not query:
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
    # print(query.query.__str__())
    data['data_pie'] = list(query)
    return JsonResponse(data)


def country(request,country_id_slug):
    data = {}
    query = Detail_Data_country.objects.filter(country_id=country_id_slug)
    data['Data'] = query
    data['LatestData'] = query.order_by('-date')[:1]
    data['country_id'] = Country.objects.get(country_code=country_id_slug)

    return render(request, 'tracker/country.html', context=data)


def country_data(request,country_id_slug):
    data = {}
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=200)
    # print(request)
    query = Detail_Data_country.objects.filter(country_id=country_id_slug,date__range=(start_date, end_date))
    fields = query.values('country_id', 'date', 'cases', 'deaths', 'total_cases', 'total_deaths')

    data['data'] = list(fields)
    return JsonResponse(data)
