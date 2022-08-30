from django import template

register = template.Library()

@register.filter
def mul(value,num):
    value=int(value)
    num=int(num)
    value=value*num
    return value