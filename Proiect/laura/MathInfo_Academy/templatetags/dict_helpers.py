from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_item(list, index):
    return list[index]

@register.filter
def round_filter(value, precision=2):
    return round(value, precision)