#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-8  上午9:59
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: updatehost.py
# @SoftWare	: PyCharm

import models

def updatehost(req):
    if req.method == "POST":
        uip=req.POST.get('ip')
        utype=int(req.POST.get('type'))-1
        ulabels=str(req.POST.get('labels')).split()
        ugip = req.POST.get('gip')
        uremarks= req.POST.get('remarks')
        res='0'
        if uip != None:
            try:
                obj=models.HostInfo.objects.filter(IP=uip)
            except Exception as e:
                print(e)
                res='未查询到该主机IP'
                return res
            try:
                if ugip:
                    obj.update(type=utype,gip=ugip,remarks=uremarks)
                else:
                    obj.update(type=utype, remarks=uremarks)
                print('1')
                for y in obj[0].labels.all():
                    print(y.id)
                    obj[0].labels.remove(y.id)
                obj[0].save()
                for lb in ulabels:
                    print(lb)
                    obj[0].labels.add(models.Services.objects.filter(service_name__contains=lb).only('id')[0])
                obj[0].save()
            except Exception as e:
                print(e)
                res="更新主机信息失败，请重试"
                return res
            return res
        else:
            res="获取的IP为空，请重试"
            return res
