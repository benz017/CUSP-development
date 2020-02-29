from django.shortcuts import render
from .models import Email
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
import os


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
def success(request):
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


