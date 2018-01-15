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

def shorturlcreation(request):
    deleteoldrecords()
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['short_url']=="":
                u = Urls(url=form.cleaned_data['url'],short_url=generateshorturl(), text_message="None", click_count=0, add_date=timezone.now())
            else:
                u = Urls(url=form.cleaned_data['url'],short_url=form.cleaned_data['short_url'], text_message="None", click_count=0, add_date=timezone.now())
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