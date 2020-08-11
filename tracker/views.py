import datetime
import os, json
import urllib.request
from django.db.models import Sum, F

from django.core.paginator import Paginator
from django.shortcuts import render

from tracker.models import Country, Detail_Data_country
from tracker.crawler import task

from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from tracking_board_project.settings import STATIC_DIR


def index(request):
    # task()
    dataset = {}

    world = Country.objects.get(country_code='OWID_WRL')
    world_summary_data = Detail_Data_country.objects.filter(country=world).order_by('-date')[:1]
    query = Detail_Data_country.objects.exclude(country=world).filter(
        date=datetime.date.today())
    if not query:
        query = Detail_Data_country.objects.exclude(country=world).filter(
            date=datetime.date.today() - datetime.timedelta(days=1))
    data = query.order_by('-total_cases')[:10]
    detail_data = query.order_by('-total_cases')
    # paginator = Paginator(dataset, 10)
    # detail_data = paginator.page(1)

    continent_data = query.values('country__continent').annotate(total_cases=Sum('total_cases'),
                                                                 total_deaths=Sum('total_deaths'),
                                                                 cases=Sum('cases'),
                                                                 deaths=Sum('deaths')).order_by('-total_cases')

    dataset['Top10_Data'] = data
    dataset['Detail'] = detail_data
    dataset['WorldData'] = world_summary_data
    dataset['Continents'] = continent_data

    return render(request, 'tracker/index.html', context=dataset)


def json_data(request):
    data = {}
    world_query = Detail_Data_country.objects.filter(country__country_code='OWID_WRL').order_by('date').values()
    q = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL').filter(
        date=datetime.date.today())
    if not q:
        q = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL').filter(
            date=datetime.date.today() - datetime.timedelta(days=1))
    country_q = q.values('country__country_name', 'cases', 'deaths', 'total_cases', 'total_deaths',
                         'cases_per_million', 'total_cases_per_million', 'deaths_per_million',
                         'total_deaths_per_million').order_by('-total_cases')[:10]

    map_query = q.annotate(code=F('country__country_2digits_code')).values()

    data['map_data'] = list(map_query)
    data['world_data'] = list(world_query)
    data['country_data'] = list(country_q)
    data['location'] = getGeolocation()

    return JsonResponse(data)


def getGeolocation():
    req = urllib.request.Request('http://ip-api.com/json/', data=None)
    response = urllib.request.urlopen(req)
    if response.code == 200:
        encoding = response.headers.get_content_charset()
        return json.loads(response.read().decode(encoding))


def chart(request):
    data = {}

    # print(query.query.__str__())
    c = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL')
    continent_query = c.values('date', 'country__continent').annotate(total_cases=Sum('total_cases'),
                                                                      total_deaths=Sum('total_deaths'),
                                                                      cases=Sum('cases'),
                                                                      deaths=Sum('deaths'))
    q = c.filter(date=datetime.date.today())
    if not q:
        q = c.filter(date=datetime.date.today() - datetime.timedelta(days=1))
    pie_query = q.values('country__continent').annotate(total_cases=Sum('total_cases'),
                                                        total_deaths=Sum('total_deaths'),
                                                        cases=Sum('cases'),
                                                        deaths=Sum('deaths'))

    data['data_pie'] = list(pie_query)
    data['data_line'] = list(continent_query)
    return JsonResponse(data)


def country(request, country_id_slug):
    data = {}
    query = Detail_Data_country.objects.filter(country_id=country_id_slug)
    data['Data'] = query
    data['LatestData'] = query.order_by('-date')[:1]
    data['country_id'] = Country.objects.get(country_code=country_id_slug)

    return render(request, 'tracker/country.html', context=data)


def country_detail(request, country_id_slug):
    data = {}
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=200)
    # print(request)
    query = Detail_Data_country.objects.filter(country_id=country_id_slug, date__range=(start_date, end_date)).order_by(
        'date')
    fields = query.values('country_id', 'date', 'cases', 'deaths', 'total_cases', 'total_deaths')
    data['data'] = list(fields)
    return JsonResponse(data)


def download(request):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file = os.path.join(STATIC_DIR, 'temp_files/detail.csv')
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="data.csv"'
    return response
