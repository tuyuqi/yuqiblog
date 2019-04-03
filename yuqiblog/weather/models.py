from django.db import models
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import get_template


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length = 25)

    def __str__(self): ##show the actual city name on the dashboard
        return self.name

    class Meta: ##show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
