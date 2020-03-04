from razorpay import Client
from datetime import datetime


def create_order(amt):
    id = 1
    now = datetime.now()
    receipt= str(datetime.timestamp(now))+"00"+str(id)
    id+=1
    client = Client(auth=("rzp_test_VS4c9ujrlnqnII","pcUrzfu6gL6PjxP7bq5Z4Uo4"))
    data = {'amount':amt,'currency':'INR','receipt':receipt,'payment_capture':1}
    response = client.order.create(data=data)
    response2 = client.invoice.create(data=data)
    print(response)
    print(response2)

create_order(100)