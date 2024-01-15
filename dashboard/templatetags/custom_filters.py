import re
from django import template
from datetime import datetime
from dateutil.parser import parse

register = template.Library()

@register.filter(name='strip_quotes')
def strip_quotes(value):
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1] 
    return value


@register.filter(name='custom_date_format')
def custom_date_format(value):
    try:
        value = parse(value)
    except (ValueError, TypeError):
        return value

    if not isinstance(value, datetime):
        return value 

    months = [
        'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
        'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
    ]
    formatted_date = f"{value.day} {months[value.month - 1]} {value.year} {value.hour:02d}:{value.minute:02d}"
    return formatted_date


@register.filter
def to_datetime(value):
    try:
        return parse(value)
    except ValueError:
        return value
    
@register.filter
def string_to_datetime(value):
    formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"]
    
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return value


@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter(name='filter_keys')
def filter_keys(value, arg):
    """
    value: sözlük (i.fields)
    arg: anahtar listesi (alan_listesi)
    """
    return {key: value[key] for key in arg if key in value}

@register.filter(name='get_attribute')
def get_attribute(value, key):
  
    if isinstance(value, dict) and key in value:
        return value.get(key)
    return ''

@register.filter
def get_value_from_dict(dictionary, key):
    return dictionary.get(key, "")