from django.template import Library
from pytz import timezone
from django.utils.safestring import mark_safe
import datetime

register = Library()  # 变量名必须是rigister


@register.simple_tag
def convert_date(sourse_date):
    tz = timezone("Asia/Shanghai")
    now = datetime.datetime.now().replace(tzinfo=tz)
    # sourse_date = datetime.datetime.strptime(sourse_date, "%Y-%m-%d %H:%M:%S.%f")
    c = now - sourse_date.replace(tzinfo=tz)
    if c.seconds/3600 > 1:
        return sourse_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return "%s分钟前" % int(c.seconds/60)
