from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
# Create your models here.

User = get_user_model()

class BookInfo(models.Model):
    title = models.CharField(max_length=256, verbose_name='Book')
    author = models.CharField(max_length=50, verbose_name='Author')
    # isbn = models.CharField(max_length=50, verbose_name='ISBN')
    price = models.CharField(max_length=10 ,verbose_name='Price')
    link = models.CharField(max_length=256, verbose_name='Link')
    # add_date = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    # mod_date = models.DateTimeField(auto_now=True, verbose_name="Modified")

    def __str__(self):
        return "{}-{}-{}".format(self.title,self.author, self.price)
