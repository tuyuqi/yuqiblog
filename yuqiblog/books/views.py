from django.shortcuts import render, redirect
from fake_useragent import UserAgent
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
import re
import os
import shutil
from datetime import timedelta, timezone, datetime

from .models import BookInfo
# Create your views here.



book_data = []

def book_spider(request):

        session = requests.Session()
        session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
        urls = ['https://www.amazon.com/best-sellers-books-Amazon/zgbs/books','https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_2?_encoding=UTF8&pg=2']

        for url in urls:
            content = session.get(url, verify=False).content
        soup = BeautifulSoup(content, 'lxml')
        posts = soup.find_all('li',{'class':'zg-item-immersion'})
        # book_data = list()

        for i in posts:
            book = {}
            link = 'https://www.amazon.com' + str(i.find_all('a',{'class':'a-link-normal'})[0]['href'])
            title = str(i.find_all('div',{'class':'p13n-sc-truncate p13n-sc-line-clamp-1'})[0].text)
            author = i.find_all('div',{'class':'a-row a-size-small'})[0].text
            # review_count = i.find_all('a',{'a-size-small a-link-normal'})[0].text
            price = str(i.find_all('span',{'class':'p13n-sc-price'})[0].text)
            # price_regexp = re.compile("\$[0-9]+(\.[0-9]{2})?") # for amazon.com
            # price = soup.find(text=price_regexp)
            new_book = BookInfo()
            new_book.title = title
            new_book.author = author
            new_book.price = price
            new_book.link = link
            new_book.save()

            books = BookInfo.objects.all()
            context = {
                'books': books
                }

            book['title'] = title
            book['author'] = author
            book['price'] = price
            book['link'] = link
            book_data.append(book)

        return render(request, 'books/bestsellersamazon.html')



def get_books(request):
    books = BookInfo.objects.all()
    context = {
        'books': books
    }
    return render(request, 'books/bestsellersamazon.html', context)
