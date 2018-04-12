#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/10  10:02
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: get_data.py
# @SoftWare	: PyCharm

from django import template
from VersionIterration import models
from django.utils.safestring import mark_safe
from hostinfo import models as hostmodels

register=template.Library()

@register.simple_tag()
def get_operateman(type):
    res = ""
    try:
        obj=models.OperateMan.objects.filter(type=type)
    except Exception as e:
        print(e)
        return mark_safe(res)
    if obj.count():
        for man in obj:
            res+='''<option value=%s>%s</option>'''%(man.name,man.name)
    return mark_safe(res)

@register.simple_tag()
def get_project():
    res = ""
    try:
        obj = hostmodels.Services.objects.all()
    except Exception as e:
        print(e)
        return mark_safe(res)
    if obj.count():
        for man in obj:
            res += '''<option value=%s>%s</option>''' % (man.service_name,man.service_name)
    return mark_safe(res)

@register.simple_tag()
def get_fabu_type():
    res=""
    try:
        obj=models.UpdateVersion.get_code_choices
    except Exception as e:
        print(e)
        mark_safe(res)
    for type in obj:
        res += '''<option value=%s>%s</option>''' %(type[0],type[1])
    return mark_safe(res)