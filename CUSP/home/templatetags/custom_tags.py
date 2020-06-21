from django import template
from datetime import datetime
import pytz
register = template.Library()


@register.filter('list_index')
def list_index(mylist,index):
    return mylist[index]


@register.filter
def index(sequence, position):
    return sequence[position]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def is_list(value):
    return isinstance(value, list)


@register.filter
def get_range(value):
    return range(value)

@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def delta(date,arg):
    now = datetime.utcnow().replace(tzinfo=pytz.timezone('Asia/Kolkata'))
    date = date.replace(tzinfo=pytz.timezone('Asia/Kolkata'))
    dif = date-now
    days = dif.days
    print(days)
    hr = date.hour
    min = date.minute
    if arg == "d":
        return days
    elif arg == "h":
        return hr
    elif arg == "m":
        return min
