# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from hostinfo import models
from get_data import *
import json
# from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def Hostlist(req):
    try:
        obj = get_all_hostlist()
        sobj = get_service_name_data()
        tobj=get_type_data()
    except Exception as e:
        print(e)
    return render(req, 'hostinfo/hostlist.html', {"hostlists":obj,'service_select':sobj,"type_select":tobj,})
def Hostadd(req):
    from addhost import host_add
    res=host_add(req)
    print(res)
    return HttpResponse(json.dumps(res))
def HostDel(req):
    from delhost import DelHost
    res=DelHost(req)
    return HttpResponse(json.dumps(res))
def addservice(req):
    if req.method == 'POST':
        res=True
        service_name=req.POST.get('cservice_name')
        tomcat_name=req.POST.get('ctomcat_name')
        try:
            if not models.Services.objects.filter(service_name=service_name,tomcat_name=tomcat_name):
                models.Services.objects.create(service_name=service_name,tomcat_name=tomcat_name)
            else:
                res="服务已经存在！"
                return HttpResponse(json.dumps(res))
        except Exception as e:
            print(e)
            res="添加服务失败，请重试！！"
    return HttpResponse(json.dumps(res))
def Dasboard(req):
    return render(req,'dashboard.html')
def filter(req):
    if req.method == "POST":
        f_type=req.POST.get('filter_type')
        f_service=req.POST.get('filter_label')
        f_service=str(f_service).encode('utf-8')
        try:
            sobj = get_service_name_data()
            tobj = get_type_data()
        except Exception as e:
            print(e)
        if f_type != 'null' and f_service != 'null':
            try:
                obj = models.HostInfo.objects.filter(type=f_type,labels__service_name__contains=f_service)
            except Exception as e:
                print('f:')
                print(e)
            return render(req, 'hostinfo/hostlist.html',
                          {"hostlists": obj, 'service_select': sobj, "type_select": tobj, })
        elif f_service != 'null' and f_type  == 'null':
            try:
                obj = models.HostInfo.objects.filter(labels__service_name__contains=f_service)
            except Exception as e:
                print('f:')
                print(e)
            return render(req, 'hostinfo/hostlist.html',
                          {"hostlists": obj, 'service_select': sobj, "type_select": tobj, })
        elif f_service == 'null' and f_type  != 'null':
            try:
                obj = models.HostInfo.objects.filter(type=f_type)
                for i in obj:
                    print(i.IP)
            except Exception as e:
                print('f:')
                print(e)
            return render(req, 'hostinfo/hostlist.html', {"hostlists":obj,'service_select':sobj,"type_select":tobj,})
        else:
            return HttpResponseRedirect('/hostinfo/hostlist')