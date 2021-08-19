from django import template

register = template.Library()
@register.filter(name='cut')
def cut(value, arg):
    per =(100*(value-arg))/value
    return str(per)[:5]
