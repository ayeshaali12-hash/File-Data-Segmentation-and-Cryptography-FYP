from django import template
import datetime

register = template.Library()

@register.filter
def format_date(value):
    if isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d')
    return value
