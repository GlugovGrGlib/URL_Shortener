from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views.generic.base import RedirectView
from .forms import URLForm, ManageForm
from datetime import datetime, timedelta
from django.utils import timezone
from urllib.parse import urlparse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
import random, string
from lxml import html
import requests
from .serializers import *
from rest_framework import generics

def shorturlcreation(request):
    deleteoldrecords()
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            text_content = getcontent(form.cleaned_data['url'])
            if form.cleaned_data['short_url']=="":
                u = Urls(url=form.cleaned_data['url'],short_url=generateshorturl(), text_message=text_content, click_count=0, add_date=timezone.now())
            else:
                u = Urls(url=form.cleaned_data['url'],short_url=form.cleaned_data['short_url'], text_message=text_content, click_count=0, add_date=timezone.now())
            u.save()
            return HttpResponseRedirect('')
    else:
        form = URLForm()
    latest_urls_list = Urls.objects.order_by('-add_date')[:5]
    context = {'latest_urls_list':latest_urls_list, 'form':form}
    return render(request, 'createshorturl.html', context)

def generateshorturl():
    length = randint(5,8)
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        short_url = ''.join(random.choice(char) for x in range(length))
        try:
            temp = Urls.objects.get(short_url=short_url)
        except:
            return short_url

def getcontent(URL):
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    text = tree.xpath('//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6 or self::p or self::span]/text()')[0]
    text_list = text.split()
    for x in range(len(text_list)):
        if len(text_list[x])==6:
            tmp_list = text_list[x].split()
            tmp_list.append('\u2122')
            text_list[x] = ''.join(tmp_list)
    content = ' '.join(text_list)
    return content

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Urls.objects.all()
    serializer_class = UrlsSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

def details(request, url_id):
    full_url = get_object_or_404(Urls, pk=url_id)
    if request.method == 'POST':
        form = ManageForm(request.POST)
        if form.is_valid():
            full_url.short_url = form.cleaned_data['short_url']
            full_url.text_message = form.cleaned_data['text_message']
            full_url.click_count = form.cleaned_data['click_count']
            full_url.add_date = form.cleaned_data['add_date']
            full_url.save()
            return HttpResponseRedirect('/manage')
    else:
        form = ManageForm( initial={'short_url' : full_url.short_url, 'text_message':full_url.text_message, 'click_count':full_url.click_count, 'add_date':full_url.add_date})
    o = urlparse(full_url.url)
    parsed_url = o.netloc + o.path + o.query
    context = {'full_url':full_url, 'form': form, 'parsed_url':parsed_url}
    return render(request, 'urlinfo.html', context)

def manageurls(request):
    deleteoldrecords()
    url_list = get_list_or_404(Urls)
    paginator = Paginator(url_list, 6)
    page = request.GET.get('page')
    urls_list = paginator.get_page(page)
    context = {'urls_list':urls_list}
    return render(request, 'manageurls.html', context)

def redirect(request, short_url):
    deleteoldrecords()
    full_url = get_object_or_404(Urls,short_url=short_url)
    full_url.click_count +=1
    full_url.save()
    return HttpResponseRedirect(full_url.url)

def delete(request, url_id):
    full_url = get_object_or_404(Urls, pk=url_id)
    full_url.delete()
    return HttpResponseRedirect('/manage')

def deleteoldrecords():
    now = timezone.now()
    daybefore = now - timedelta(days=14)
    oldrecords =  Urls.objects.filter(add_date__lt=daybefore)
    oldrecords.delete()
