import datetime
import json
import os
import urllib.request

from django.db.models import Sum, F, Q
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render

from tracker.models import Country, Detail_Data_country
from tracking_board_project.settings import STATIC_DIR

_latest_date = Detail_Data_country.objects.all().values('date').order_by('-date')[:1]


def index(request):
    """
    Index page shows the home page that is constructed with three parts
    Overview: Global summary data
    Region View: View by Continent
    Table Data: View by Country

    """

    dataset = {}
    world = Country.objects.get(country_code='OWID_WRL')
    world_summary_data = Detail_Data_country.objects.filter(country=world).order_by('-date')[:1]

    query = Detail_Data_country.objects.exclude(country=world).filter(
        date=_latest_date[0]['date'])

    detail_data = query.order_by('-total_cases')
    continent_data = query.values('country__continent').annotate(total_cases=Sum('total_cases'),
                                                                 total_deaths=Sum('total_deaths'),
                                                                 cases=Sum('cases'),
                                                                 deaths=Sum('deaths')).order_by('-total_cases')

    dataset['WorldData'] = world_summary_data
    dataset['Detail'] = detail_data
    dataset['Continents'] = continent_data

    return render(request, 'tracker/index.html', context=dataset)


def json_data(request):
    """
    API for delivering the global and country data to the frontend

    """
    data = {}
    world_query = Detail_Data_country.objects.filter(country__country_code='OWID_WRL').order_by('date').values()
    q = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL').filter(
        date=_latest_date[0]['date'])

    country_q = q.values('country__country_name', 'cases', 'deaths', 'total_cases', 'total_deaths',
                         'cases_per_million', 'total_cases_per_million', 'deaths_per_million',
                         'total_deaths_per_million').order_by('-total_cases')[:10]

    data['world_data'] = list(world_query)
    data['country_data'] = list(country_q)

    return JsonResponse(data)


def getGeoLocation(request):
    """
    Get the users'location via IP

    """
    data = {}
    req = urllib.request.Request('http://ip-api.com/json/', data=None)
    response = urllib.request.urlopen(req)
    if response.code == 200:
        encoding = response.headers.get_content_charset()
        data['location'] = json.loads(response.read().decode(encoding))

    return JsonResponse(data)


def map(request):
    """
    API for the map data
    """
    data = {}
    q = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL').filter(
        date=_latest_date[0]['date'])
    map_query = q.annotate(code=F('country__country_2digits_code')).values()
    data['map_data'] = list(map_query)
    return JsonResponse(data)


def chart(request):
    """
    API for the graphs and charts
    """
    data = {}

    c = Detail_Data_country.objects.exclude(country__country_code='OWID_WRL')
    continent_query = c.values('date', 'country__continent').annotate(total_cases=Sum('total_cases'),
                                                                      total_deaths=Sum('total_deaths'),
                                                                      cases=Sum('cases'),
                                                                      deaths=Sum('deaths'))
    # latest_date = Detail_Data_country.objects.all().values('date').order_by('-date')[:1]
    q = c.filter(date=_latest_date[0]['date'])
    pie_query = q.values('country__continent').annotate(total_cases=Sum('total_cases'),
                                                        total_deaths=Sum('total_deaths'),
                                                        cases=Sum('cases'),
                                                        deaths=Sum('deaths'))

    data['data_pie'] = list(pie_query)
    data['data_line'] = list(continent_query)
    return JsonResponse(data)


def country(request, country_id_slug):
    """
    Retrieve the country by country 2 digit code
    :param country_id_slug: 2 digit country code

    """
    data = {}
    query = Detail_Data_country.objects.filter(country_id__country_2digits_code=country_id_slug)
    data['Data'] = query
    data['LatestData'] = query.order_by('-date')[:1]
    data['country_id'] = Country.objects.get(country_2digits_code=country_id_slug)

    return render(request, 'tracker/country.html', context=data)


def country_detail(request, country_id_slug):
    """
    API to retrieve the country by country 2 digit code and process to the frontend
    :param country_id_slug: 2 digit country code

    """
    data = {}
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=300)
    # print(request)
    query = Detail_Data_country.objects.filter(country_id__country_2digits_code=country_id_slug,
                                               date__range=(start_date, end_date)).order_by(
        'date')
    fields = query.values('country_id', 'date', 'cases', 'deaths', 'total_cases', 'total_deaths')
    data['data'] = list(fields)
    return JsonResponse(data)


def download(request):
    """
    Download the data to csv file from the website
    """
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
    """
    Search by Country
    """
    query = Country.objects.get(country_name=request.GET.get('value')).country_2digits_code
    print(query)
    if query:
        return JsonResponse({'status': 'success', 'value': query})
    else:
        return JsonResponse({'status': 'failed'})


def autocomplete(request):
    """
    autocomplete function with search bar
    """
    response_data = {}
    input_data = request.GET.get('key')

    country_list = Country.objects.filter(Q(country_code__contains=input_data) | Q(country_name__contains=input_data))
    response_data['countryList'] = [Country.country_name for Country in country_list]

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def index_mobile(request):
    """
    Mobile version: some elements have been simplified
    """
    dataset = {}

    world = Country.objects.get(country_code='OWID_WRL')
    world_summary_data = Detail_Data_country.objects.filter(country=world).order_by('-date')[:1]
    query = Detail_Data_country.objects.exclude(country=world).filter(
        date=_latest_date[0]['date'])

    detail_data = query.order_by('-total_cases')
    continent_data = query.values('country__continent').annotate(total_cases=Sum('total_cases'),
                                                                 total_deaths=Sum('total_deaths'),
                                                                 cases=Sum('cases'),
                                                                 deaths=Sum('deaths')).order_by('-total_cases')

    dataset['Detail'] = detail_data
    dataset['WorldData'] = world_summary_data
    dataset['Continents'] = continent_data

    return render(request, 'tracker/index_mobile.html', context=dataset)


def country_mobile(request, country_id_slug):
    """
    Mobile version
    """
    data = {}
    query = Detail_Data_country.objects.filter(country_id__country_2digits_code=country_id_slug)
    data['Data'] = query
    data['LatestData'] = query.order_by('-date')[:1]
    data['country_id'] = Country.objects.get(country_2digits_code=country_id_slug)

    return render(request, 'tracker/country_mobile.html', context=data)
