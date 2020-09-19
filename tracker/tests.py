import os
from django.test import TestCase
from requests import Session
from datetime import datetime
from tracker.models import Country, Detail_Data_country
from django.urls import reverse
from django.db.models.query import QuerySet
from tracking_board_project.settings import STATIC_DIR
from .crawler import get_detail_data, store_detail_data


class TrackerTests(TestCase):
    def setUp(self):
        """
        Initial basic data
        """
        world = Country(country_code='OWID_WRL', country_name='test', population_density=1)
        world.save()
        country = Country(country_code='TEW', country_name='test01', population_density=1, country_2digits_code='TE')
        country.save()
        daily_data_world = Detail_Data_country(date='2020-2-20', country=world, cases=1, total_cases=2,
                                               deaths=0, total_deaths=1, cases_per_million=1,
                                               total_cases_per_million=1.0,
                                               deaths_per_million=1, total_deaths_per_million=1)
        daily_data_world.save()
        daily_data_country = Detail_Data_country(date='2020-2-20', country=country, cases=1, total_cases=2,
                                                 deaths=0, total_deaths=1, cases_per_million=1,
                                                 total_cases_per_million=1.0,
                                                 deaths_per_million=1, total_deaths_per_million=1)
        daily_data_country.save()

        self.response = self.client.get(reverse('tracker:index'))
        self.detail_response = self.client.get('/tracker/country/TE/')

    def test_index_page_response(self):
        """
        Test whether the index page requesting is correct
        """
        self.assertEqual(self.response.status_code, 200)

    def test_country_page_response(self):
        """
        Test whether the country page requesting is correct
        """
        self.assertEqual(self.detail_response.status_code, 200, "Requesting the detail country page failed.")

    def test_template_filename(self):
        """
        Test whether the pages used the correct html files
        """
        self.assertTemplateUsed(self.response, 'tracker/index.html')
        self.assertTemplateUsed(self.detail_response, 'tracker/country.html')

        index_mobile = self.client.get('/tracker/mobile/')
        self.assertTemplateUsed(index_mobile, 'tracker/index_mobile.html')

        country_mobile = self.client.get('/tracker/mobile/country/TE/')
        self.assertTemplateUsed(country_mobile, 'tracker/country_mobile.html')

    def test_index_page_context(self):
        """
        Test the index page context is satisfied
        """
        expected_world_data = list(
            Detail_Data_country.objects.filter(country__country_code='OWID_WRL').order_by('-date')[:1])
        self.assertEqual(expected_world_data, list(self.response.context['WorldData']))
        self.assertEqual(type(self.response.context['Detail']), QuerySet)
        self.assertEqual(type(self.response.context['Continents']), QuerySet)

    def test_detail_page_context(self):
        """
        Test the detail page context whether it is satisfied
        """
        expected_country_data = list(Detail_Data_country.objects.filter(country__country_code='TEW'))
        self.assertEqual(expected_country_data, list(self.detail_response.context['Data']))
        self.assertEqual(type(self.detail_response.context['LatestData']), QuerySet)

    def test_crawl_data(self):
        """
        Test the crawl function  whether it is working
        """
        session = Session()
        urls = ['https://covid.ourworldindata.org/data/owid-covid-data.csv',
                'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv']
        now = datetime.now()
        detail_csv = os.path.join(STATIC_DIR, 'temp_files/detail.csv')
        ret = get_detail_data(session, urls, detail_csv)
        self.assertTrue(ret)
        csv_fileinfo = os.stat(detail_csv)
        create_time = datetime.fromtimestamp(csv_fileinfo.st_ctime)
        self.assertGreater(create_time, now)

    def test_store_detail_data(self):
        """
        Test the data store process is working or not
        """
        self.assertTrue(store_detail_data(2))
