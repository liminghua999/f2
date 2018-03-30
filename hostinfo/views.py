# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from hostinfo import models
from get_data import *


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
    res=host_add()
    return HttpResponse(res)
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