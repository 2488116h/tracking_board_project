import datetime
import os, json
import urllib.request
from django.db.models import Sum, F, Q

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse

from tracker.models import Country, Detail_Data_country
from tracker.crawler import task

from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from tracking_board_project.settings import STATIC_DIR


def index(request):
    # task()
    dataset = {}

    world = Country.objects.get(country_code='OWID_WRL')
    world_summary_data = Detail_Data_country.objects.filter(country=world).order_by('-date')[:1]
    latest_date = Detail_Data_country.objects.all().values('date').order_by('-date')[:1]
    query = Detail_Data_country.objects.exclude(country=world).filter(
        date=latest_date[0]['date'])

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

    latest_date = Detail_Data_country.objects.all().values('date').order_by('-date')[:1]
    q = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL').filter(
        date=latest_date[0]['date'])

    country_q = q.values('country__country_name', 'cases', 'deaths', 'total_cases', 'total_deaths',
                         'cases_per_million', 'total_cases_per_million', 'deaths_per_million',
                         'total_deaths_per_million').order_by('-total_cases')[:10]

    map_query = q.annotate(code=F('country__country_2digits_code')).values()

    def getGeoLocation():
        req = urllib.request.Request('http://ip-api.com/json/', data=None)
        response = urllib.request.urlopen(req)
        if response.code == 200:
            encoding = response.headers.get_content_charset()
            return json.loads(response.read().decode(encoding))

    data['map_data'] = list(map_query)
    data['world_data'] = list(world_query)
    data['country_data'] = list(country_q)
    data['location'] = getGeoLocation()

    return JsonResponse(data)


def chart(request):
    data = {}

    # print(query.query.__str__())
    c = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL')
    continent_query = c.values('date', 'country__continent').annotate(total_cases=Sum('total_cases'),
                                                                      total_deaths=Sum('total_deaths'),
                                                                      cases=Sum('cases'),
                                                                      deaths=Sum('deaths'))
    latest_date = Detail_Data_country.objects.all().values('date').order_by('-date')[:1]
    q = c.filter(date=latest_date[0]['date'])
    pie_query = q.values('country__continent').annotate(total_cases=Sum('total_cases'),
                                                        total_deaths=Sum('total_deaths'),
                                                        cases=Sum('cases'),
                                                        deaths=Sum('deaths'))

    data['data_pie'] = list(pie_query)
    data['data_line'] = list(continent_query)
    return JsonResponse(data)


def country(request, country_id_slug):
    data = {}
    query = Detail_Data_country.objects.filter(country_id__country_2digits_code=country_id_slug)
    data['Data'] = query
    data['LatestData'] = query.order_by('-date')[:1]
    data['country_id'] = Country.objects.get(country_2digits_code=country_id_slug)

    return render(request, 'tracker/country.html', context=data)


def country_detail(request, country_id_slug):
    data = {}
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=200)
    # print(request)
    query = Detail_Data_country.objects.filter(country_id__country_2digits_code=country_id_slug,
                                               date__range=(start_date, end_date)).order_by(
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


def search_bar(request):
    query = Country.objects.get(country_name=request.GET.get('value')).country_2digits_code
    print(query)
    if query:
        return JsonResponse({'status': 'success', 'value': query})
    else:
        return JsonResponse({'status': 'failed'})


def autocomplete(request):
    response_data = {}
    input_data = request.GET.get('key')

    country_list = Country.objects.filter(Q(country_code__contains=input_data) | Q(country_name__contains=input_data))
    response_data['countryList'] = [Country.country_name for Country in country_list]

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def index_mobile(request):
    dataset = {}

    world = Country.objects.get(country_code='OWID_WRL')
    world_summary_data = Detail_Data_country.objects.filter(country=world).order_by('-date')[:1]
    latest_date = Detail_Data_country.objects.all().values('date').order_by('-date')[:1]
    query = Detail_Data_country.objects.exclude(country=world).filter(
        date=latest_date[0]['date'])

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

    return render(request, 'tracker/index_mobile.html', context=dataset)


def country_mobile(request, country_id_slug):
    data = {}
    query = Detail_Data_country.objects.filter(country_id__country_2digits_code=country_id_slug)
    data['Data'] = query
    data['LatestData'] = query.order_by('-date')[:1]
    data['country_id'] = Country.objects.get(country_2digits_code=country_id_slug)

    return render(request, 'tracker/country_mobile.html', context=data)
