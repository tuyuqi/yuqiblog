from __future__ import absolute_import, unicode_literals
from celery import task
from django.core.mail import send_mail
import time
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
from pytz import timezone
import requests
from celery.decorators import periodic_task
from celery.task.schedules import crontab

#@task
@periodic_task(
    run_every=(crontab(hour=7, minute=30)),
    name="task_mail",
    ignore_result=True
)
def task_mail():

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=bdb2fc4dceba425650a3e1fea845179c'
    tf = TimezoneFinder(in_memory=True)
    utc = pytz.utc
    city = 'New York'
    city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
    now_utc = utc.localize(datetime.utcfromtimestamp(city_weather['dt']))
    weather = {
            'city' : city,
            'temperature' : city_weather['main']['temps'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            ##'tisme' : datetime.fromtimestamp(city_weather['dt']).strftime('%Y-%m-%d'),
            'date' : now_utc.astimezone(timezone(tf.timezone_at(lng=city_weather['coord']['lon'], lat=city_weather['coord']['lat']))).strftime('%Y-%m-%d')
    }

    subject = "Today's weather in NYC"
    message = "Today is " + str(weather["date"])+ ". The weather in " + weather["city"] + " is " + weather["description"] +" with the temperature: " + str(weather["temperature"]) + " °F."
    mail_sent = send_mail(subject,
                          message,
                          'yuqi_tu@hotmail.com',
                          ['yt2604@cumc.columbia.edu','yuqi_tu@hotmail.com'])
    return mail_sent
