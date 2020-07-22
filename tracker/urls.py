from django.urls import path
from tracker import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('continent_data/',views.chart,name='continent_data'),
    path('country_data/',views.country,name = 'country_data')
    ]