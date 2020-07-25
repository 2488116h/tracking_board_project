from django.urls import path
from tracker import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('continent_data/',views.chart,name='continent_data'),
    path('country/<slug:country_id_slug>/',views.country,name = 'country'),
    path('country_detail/<slug:country_id_slug>/',views.country_data, name = 'country_detail'),
    ]