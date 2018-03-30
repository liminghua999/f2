
from django import template

register=template.Library()

# @register.simple_tag()
# def Get_choice(obj):
#     return obj._meta.