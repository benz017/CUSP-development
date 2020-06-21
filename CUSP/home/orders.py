from razorpay import Client
import itertools
from datetime import datetime
from django.conf import settings


#client = Client(auth=(settings.RAZOR_PAY_KEY,settings.RAZOR_PAY_SECRET_KEY))
client = Client(auth=('rzp_test_B6VZbXYKqGebNh','R9119fSHs00gQfhewsfJJUvg'))
base_URL = 'https://api.razorpay.com/v1'#settings.RAZOR_PAY_API
Header = {'content-type':'application/json'}


def counter(start, interval):
    count = start
    while True:
        yield count
        count += interval


count = counter(start=1, interval=1)


def autoIncrement():
    return str(next(count)).zfill(3)


def create_order(amt):
    now=datetime.now()
    receipt = str(int(datetime.timestamp(now)))+"-"+autoIncrement()
    amt = str(amt)+"00"
    data = {'amount':amt,'currency':'INR','receipt':receipt,'payment_capture':1}
    response = client.order.create(data=data)
    return response


def create_customer(user):
    url = '/customers'
    data = {"name": "Gaurav Kumar", "email": "gaurav.kumar@example.com", "contact": "9123456789",}