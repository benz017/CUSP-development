from razorpay import Client
from datetime import datetime
from django.conf import settings


client = Client(auth=('rzp_test_zgJPhTveo69gTo','fLdjrN73LUY7aZHdRYusDdzL'))


def create_order(amt):
    id = 1
    receipt= "00"+str(id)
    id+=1
    data = {'amount':amt,'currency':'INR','receipt':receipt,'payment_capture':1}
    response = client.order.create(data=data)   
    return response