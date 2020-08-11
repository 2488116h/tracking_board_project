from django.urls import path,re_path
from tracker import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('continent_data/',views.chart,name='continent_data'),
    path('country/<slug:country_id_slug>/',views.country,name = 'country'),
    path('country_detail/<slug:country_id_slug>/',views.country_detail, name = 'country_detail'),
    # path('country_data/',views.country_data,name='country_data'),
    path('json_data/',views.json_data,name='json_data'),
    path('download/',views.download,name = 'file_download'),
    # path('location/',views.getGeolocation,name = 'location'),

    ]