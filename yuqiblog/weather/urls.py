#the_weather/weather/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.weather_index, name='weather'),
    path('task_use_celery', views.task_use_celery, name='task_use_celery')
]
