from django.shortcuts import render
from .models import Events,Subscribers
from .timer import time,date,earlybird_time
from .pricing import discount_calculator
from .text_processing import para_splitter
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from razorpay import Client
import json
# Create your views here.
client = Client(auth=(settings.RAZOR_PAY_KEY,settings.RAZOR_PAY_SECRET_KEY))


def landing(request):
    json_data = {}
    event = Events.objects.all()
    last_obj = Events.objects.last()
    json_data['event'] = event
    json_data['start_time'] = time(Events)
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
    if request.method == "POST":
        Subscribers.email = request.POST['email']
        Subscribers.objects.create(email=Subscribers.email)
        subject = 'New Subscriber'
        msg = 'New member added to our family, don\'t let them down. \nEmail-ID: ' + Subscribers.email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    return render(request,'home/index.html', context=json_data)

@csrf_exempt
def pay(request):
    if request.method == "POST":
        amount = 5100
        payment_id = request.form['razorpay_payment_id']
        client.payment.capture(payment_id, amount)
        pay_id = json.dumps(client.payment.fetch(payment_id))
        print(pay_id)
    return render(request,'home/index.html')

@csrf_exempt
def success(request):
    if request.method == "POST":
        Subscribers.email = request.POST['email']
        subject = 'Acknowledgement Mail'
        name = Subscribers.email.split('@')[0]
        html_content = render_to_string('contact/ackmail.html',
                                        {'name': name, 'subject': subject})  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [Subscribers.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse('Acknowledgement mail sent')


def products(request):
    if request.method == "POST":
        Subscribers.email = request.POST['email']
        Subscribers.objects.create(email=Subscribers.email)
        subject = 'New Subscriber'
        msg = 'New member added to our family, don\'t let them down. \nEmail-ID: ' + Subscribers.email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    return render(request, '404.html',{'bg_url':'img/404/bg01.jpg'})


def events(request):
    if request.method == "POST":
        Subscribers.email = request.POST['email']
        Subscribers.objects.create(email=Subscribers.email)
        subject = 'New Subscriber'
        msg = 'New member added to our family, don\'t let them down. \nEmail-ID: ' + Subscribers.email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    return render(request, '404.html',{'bg_url':'img/404/bg02.jpg'})


def blogs(request):
    if request.method == "POST":
        Subscribers.email = request.POST['email']
        Subscribers.objects.create(email=Subscribers.email)
        subject = 'New Subscriber'
        msg = 'New member added to our family, don\'t let them down. \nEmail-ID: ' + Subscribers.email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    return render(request, '404.html',{'bg_url':'img/404/bg05.jpg'})


