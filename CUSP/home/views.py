from django.shortcuts import render
from .models import Events
import json
from django.core import serializers
from .timer import time,date,earlybird_time
from .pricing import discount_calculator
from .text_processing import para_splitter
# Create your views here.


def landing(request):
    json_data = {}
    event = Events.objects.all()
    last_obj = Events.objects.last()
    json_data['event'] = event
    json_data['start_time'] = time(last_obj)
    json_data['span'] = date(last_obj)
    if earlybird_time(last_obj):
        solo,duet,tribe = discount_calculator(last_obj)
    else:
        solo = last_obj.solo_price
        duet = last_obj.duet_price
        tribe = last_obj.tribe_price
    json_data['solo'] = solo
    json_data['duet'] = duet
    json_data['tribe'] = tribe
    json_data['about_1'], json_data['about_2'] = para_splitter(last_obj.about)
    #timer.week, timer.day, timer.hour, timer.minute, timer.second = time('01-01-2020 03:30 PM')
    return render(request,'home/index.html', context=json_data)


def products(request):
    return render(request, '404.html',{'bg_url':'img/404/bg01.jpg'})


def events(request):
    return render(request, '404.html',{'bg_url':'img/404/bg02.jpg'})


def blogs(request):
    return render(request, '404.html',{'bg_url':'img/404/bg05.jpg'})


