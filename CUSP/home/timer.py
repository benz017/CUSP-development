from datetime import datetime,timedelta
import pytz
from .models import Events


def time(all_obj):
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    frm = '%Y/%m/%d %H:%M:%S'
    objs = all_obj.objects.filter(start_date__gt=now).order_by('start_date').first()
    next_event = objs.start_date.strftime(frm)
    return next_event


def date(last_obj):
    frm_s = "%d"
    frm_e = "%d %B %Y"
    start_date = last_obj.start_date
    end_date = last_obj.end_date
    start = start_date.strftime(frm_s)
    end = end_date.strftime(frm_e)
    if start == end.split()[0]:
        span = end
    else:
        span = start + '-' + end
    return span


def earlybird_time(last_obj):
    frm = "%Y-%m-%d %H:%M:%S"
    eb_time = last_obj.earlybird_last_date
    ebt = datetime.strptime(str(eb_time)+' 23:59:58', frm)
    now = datetime.now()
    if now > ebt:
        return False
    else:
        return True

