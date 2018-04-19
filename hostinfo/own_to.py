#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-19  下午4:21
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: own_to.py
# @SoftWare	: PyCharm
import models
from django.db.models import Q
from run_an.run_shell import shell_info
def own_to():
    try:
        obj=models.HostInfo.objects.filter(type=0).values_list('IP',flat=True)
    except Exception as e:
        print(e)
    if obj:
        print('9')
        for kvmip in obj:
            macclass=shell_info(kvmip,'cat /sys/class/net/vnet*/address','shell')
            macclass.give_result()
            res=macclass.get_info()
            print('10')
            print(list(res))
            for mac in list(res):
                try:
                    qobj = models.HostInfo.objects.filter(Q(Q(mac=mac) & Q(own_to=None)))
                except Exception as e:
                    print(e)
                if qobj:
                    qobj.update(own_to=kvmip)

