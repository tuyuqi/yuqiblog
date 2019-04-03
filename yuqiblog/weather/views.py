from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
import time
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
from pytz import timezone
from django.core.mail import send_mail
from django.shortcuts import render
from .tasks import task_mail


def weather_index(request):
    cities = City.objects.all() #return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=bdb2fc4dceba425650a3e1fea845179c'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()

    weather_data = []
    tf = TimezoneFinder(in_memory=True)
    utc = pytz.utc

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        now_utc = utc.localize(datetime.utcfromtimestamp(city_weather['dt']))
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            ##'time' : datetime.fromtimestamp(city_weather['dt']).strftime('%Y-%m-%d'),
            'date' : now_utc.astimezone(timezone(tf.timezone_at(lng=city_weather['coord']['lon'], lat=city_weather['coord']['lat']))).strftime('%Y-%m-%d')
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/weather_index.html', context) #returns the index.html template


def task_use_celery(request):
    task_mail.delay()
    return render(request,
                  'weather/email_sent.html')
