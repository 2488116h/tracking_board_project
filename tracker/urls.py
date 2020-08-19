from django.urls import path
from tracker import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('continent_data/', views.chart, name='continent_data'),
    path('country/<slug:country_id_slug>/', views.country, name='country'),
    path('country_detail/<slug:country_id_slug>/', views.country_detail, name='country_detail'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('json_data/', views.json_data, name='json_data'),
    path('download/', views.download, name='file_download'),
    path('search/', views.search_bar, name='search'),
    path('m_version/', views.index_mobile, name='mobile_version'),
    path('m_version/country/<slug:country_id_slug>/', views.country_mobile, name='country_mobile_version'),
]
