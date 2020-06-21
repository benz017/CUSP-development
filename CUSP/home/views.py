from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from urllib.parse import urlencode
from django.template.defaulttags import register
from .templatetags import custom_tags
from datetime import  datetime
from django.core.serializers.json import DjangoJSONEncoder
from .models import Events,Subscribers,Email,Profile,ExpPayment
from .timer import time,date,earlybird_time
from .pricing import discount_calculator
from .text_processing import para_splitter
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template import RequestContext
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import SignUpForm,LogInForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from razorpay import Client
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from .orders import create_order
import avinit
from .utils import profile_strength
import os
# Create your views here.
client = Client(auth=(settings.RAZOR_PAY_KEY,settings.RAZOR_PAY_SECRET_KEY))


@csrf_exempt
def landing(request):
    json_data = {}
    event = Events.objects.order_by('start_date')
    recent_event = Events.objects.filter(start_date__gt=datetime.now()).order_by('start_date')
    recent_obj = Events.objects.filter(start_date__gt=datetime.now()).order_by('start_date')[0]
    json_data['event'] = recent_event
    json_data['all_event'] = event
    json_data['start_time'] = time(Events)
    json_data['span'] = date(recent_obj)
    json_data['about_1'], json_data['about_2'] = para_splitter(recent_obj.about)
    if request.method == "POST":
        if 'email' in request.POST:
            Subscribers.email = request.POST['email']
            Subscribers.objects.create(email=Subscribers.email)
            subject = 'New Subscriber'
            msg = 'New member added to our family, don\'t let them down. \nEmail-ID: ' + Subscribers.email
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    return render(request,'home/index.html', context=json_data)


@csrf_exempt
def sub_success(request):
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
    json_data = {}
    event = Events.objects.order_by('start_date')
    recent_event = Events.objects.filter(start_date__gt=datetime.now()).order_by('start_date')
    recent_obj = Events.objects.filter(start_date__gt=datetime.now()).order_by('start_date')[0]
    json_data['event'] = recent_event
    json_data['all_event'] = event
    json_data['start_time'] = time(Events)
    json_data['span'] = date(recent_obj)
    json_data['about_1'], json_data['about_2'] = para_splitter(recent_obj.about)
    return render(request, 'event/index.html', context=json_data)


def blogs(request):
    if request.method == "POST":
        Subscribers.email = request.POST['email']
        Subscribers.objects.create(email=Subscribers.email)
        subject = 'New Subscriber'
        msg = 'New member added to our family, don\'t let them down. \nEmail-ID: ' + Subscribers.email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    return render(request, '404.html',{'bg_url':'img/404/bg05.jpg'})


def contact(request):
    if request.method == "POST":
        Email.name = request.POST['name']
        Email.email = request.POST['email']
        Email.contact_number = request.POST['contact_number']
        Email.message = request.POST['message']
        Email.objects.create(
            name=Email.name,
            email=Email.email,
            contact_number=Email.contact_number,
            message=Email.message
            )
        subject = Email.name + ' - ' + Email.email
        msg = 'Name: ' + Email.name + '\nEmail-ID: ' + Email.email + '\nContact Number: ' + Email.contact_number + '\n\n\n' + Email.message
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
    return render(request,'contact/index.html')


@csrf_exempt
def con_success(request):
    print(request)
    if request.method == "POST":
        Email.name = request.POST['name']
        Email.email = request.POST['email']
        subject = 'Acknowledgement Mail'
        html_content = render_to_string('contact/ackmail.html', {'name': Email.name, 'subject': subject})  # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [Email.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse('Acknowledgement mail sent')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['terms']:
                user = form.save()
                user.refresh_from_db()
                name = form.cleaned_data.get('name').split()
                user.profile.first_name = user.first_name = name[0]
                user.profile.last_name = user.last_name = ' '.join(name[1:])
                user.profile.email = form.cleaned_data.get('email')
                user.profile.username = form.cleaned_data.get('username')
                user.profile.password = form.cleaned_data.get('password2')
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Please Activate Your Account'
                # load a template like get_template() 
                # and calls its render() method immediately.
                message = render_to_string('signup/activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                messages.info(request, "* Kindly check your email for the Verification Link.")
            else:
                messages.info(request, "* Accept the Terms of Services to proceed.")
    else:
        form = SignUpForm()
    return render(request, 'signup/index.html', {'form':form, 'action':'signup'})


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        auth_login(request, user, backend)
        return redirect("index")
    else:
        return HttpResponseNotFound('activation_invalid.html')


def signin(request):
    if request.method == "POST":
        form = LogInForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(username=username)
            user = authenticate(request, username=username,password=password)
            if user is not None:          
                    auth_login(request, user)
                    return redirect('index')
            elif user_obj.is_active is False:
                    messages.error(request,"* Verify your Email ID using the verification link sent.")
                    messages.error(request,"* Your account might be disabled")          
            else:
                messages.error(request, '* Invalid credentials.')
                return redirect('signin')
        except:
            messages.error(request, '* User does not exist. Please Sign Up.')
            return redirect('signup')
    else:
        form = LogInForm()
    return render(request, 'signup/index.html', {'form':form , 'action':'login'})


def signout(request):
    auth_logout(request)
    return redirect("index")


def login_cancelled(request):
    return redirect(request, 'signin')

@csrf_exempt
@login_required
def account(request):
    pid = Profile.objects.filter(user=request.user.profile.user)
    profile = json.dumps(list(pid.values()),indent=4, cls=DjangoJSONEncoder)
    c=0
    data = {}
    for k,v in json.loads(profile)[0].items():
        if k not in ["signup_confirmation","id","user_id","avatar"]:
            if v in [None, '']:
                data[k] = ""
            elif k in ['languages','places_visited','passion','allergic_food','physical_activities','health_problems']:
                import ast
                v = ast.literal_eval(v)
                data[k] = v
            else:
                data[k] = v
            if v not in [None, '', "[]", "0", "+91-",[]]:
                print(v)
                c += 1
    print(c)
    data["ps"], data["psp"] = profile_strength(c)
    av = pid.values_list("avatar", flat=True)[0]
    print(av)
    if av == "":
        name = request.user.get_full_name()
        data["avatar"] = avinit.get_avatar_data_url(name)
    else:
        data["avatar"] = settings.MEDIA_URL+av
    if request.method == "POST":
        if 'imgbase64' in request.POST:
            imgdata = request.POST.get('imgbase64')
            import base64
            from PIL import Image
            from io import BytesIO
            from django.core.files.uploadedfile import InMemoryUploadedFile
            imgdata=imgdata.replace("data:image/png;base64,","")+"=="
            im = Image.open(BytesIO(base64.b64decode(imgdata)))
            url = "avatar/"+request.user.profile.username+".png"
            im.save("media/"+url, 'PNG')
            pid = Profile.objects.filter(user=request.user.profile.user)
            print(pid)
            pid.update(avatar=url)

        else:
            dt_frm = "%Y-%m-%d"
            fn = request.POST.get('first-name')
            ln = request.POST.get('last-name')
            #un = request.POS.getT['username')
            cn = request.POST.get('contact')
            dt = request.POST.get('datetime') or None
            lo = request.POST.get('location')
            rs = request.POST.get('rel-status')
            es = request.POST.get('emp-status')
            pr = request.POST.get('profession')
            di = request.POST.get('diet')
            py = request.POST.get('persona')
            pa = list(filter(lambda a: a != "", request.POST.getlist('passion')))
            lg = list(filter(lambda a: a != "", request.POST.getlist('language')))
            vi = list(filter(lambda a: a != "", request.POST.getlist('visited')))
            al = list(filter(lambda a: a != "", request.POST.getlist('allergy')))
            ac = list(filter(lambda a: a != "", request.POST.getlist('activities')))
            hl = list(filter(lambda a: a != "", request.POST.getlist('health')))
            bio = request.POST.get('bio')
            print(lg , pa, vi, al, ac, hl)
            pid = Profile.objects.filter(user=request.user.profile.user)
            print(pid)
            #dt = datetime.strptime(dt,dt_frm)
            pid.update(user=request.user, first_name= fn,last_name=ln,contact_number=cn,dob=dt, location=lo, relationship_status=rs,
                                   languages=lg, passion=pa, places_visited=vi,emp_status=es, profession=pr, diet=di,
                                   allergic_food=al,physical_activities=ac,health_problems=hl,
                                   personality=py, bio=bio)
            return redirect('account')

    return render(request, 'account/index.html', context=data)

@login_required
def myorders(request):
    data= {}
    pid = Profile.objects.filter(user=request.user.profile.user)
    data['profile'] = pid
    pay_id = ExpPayment.objects.order_by('-updated_at').filter(user=request.user.profile.id)
    data['payments'] = pay_id
    av = pid.values_list("avatar", flat=True)[0]
    if av == "":
        name = request.user.get_full_name()
        data["avatar"] = avinit.get_avatar_data_url(name)
    else:
        data["avatar"] = settings.MEDIA_URL + av
    return render(request, 'account/order.html', context=data)

@login_required
def mycalender(request):
    data = {}
    pid = Profile.objects.filter(user=request.user.profile.user)
    events = Events.objects.all()
    data['events'] = events
    av = pid.values_list("avatar", flat=True)[0]
    if av == "":
        name = request.user.get_full_name()
        data["avatar"] = avinit.get_avatar_data_url(name)
    else:
        data["avatar"] = settings.MEDIA_URL + av
    return render(request, 'account/calendar.html', context=data)
