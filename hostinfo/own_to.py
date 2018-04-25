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
    if obj.exists():
        for kvmip in obj:
            print('kvmip: '+kvmip)
            macclass=shell_info(kvmip,'cat /sys/class/net/vnet*/address','shell')
            macclass.give_result()
            res=macclass.get_info()
            maclist=[]
            tmpmac=''
            for i in res:
                if str(i) == '\n':
                    maclist.append(tmpmac)
                    tmpmac = ''
                    continue
                tmpmac+=str(i)
            print(maclist)
            for mac in maclist:
                rmac=mac.replace('fe','52',1)
                print(rmac)
                try:
                    qobj = models.HostInfo.objects.filter(Q(Q(mac__iexact=rmac) & Q(own_to=None)))
                except Exception as e:
                    print(e)
                if qobj.exists():
                    try:
                        qobj.update(own_to=kvmip)
                        for i in qobj:
                            i.save()
                    except Exception as e:
                        print('update kvm-vm failed')
                        print(e)
                else:
                    print(rmac+': filter none')

