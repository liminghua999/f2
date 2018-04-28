# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from get_data import *
import json
# from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
from login.views import Login_req

@Login_req
def Hostlist(req):
    res = {'data': {'filter_type': None, 'filter_service': None}, 'err': '0'}
    from login.get_login_username import get_login_username
    username=get_login_username(req)
    try:
        obj = get_all_hostlist()
        sobj = get_service_name_data()
        tobj=get_type_data()
    except Exception as e:
        print(e)
    return render(req, 'hostinfo/hostlist.html', {"hostlists":obj,'service_select':sobj,"type_select":tobj,'cu':username,'filtervalue':res,})
@Login_req
def Hostadd(req):
    from addhost import host_add
    res=host_add(req)
    print(res)
    return HttpResponse(json.dumps(res))
@Login_req
def HostDel(req):
    from delhost import DelHost
    res=DelHost(req)
    return HttpResponse(json.dumps(res))
@Login_req
def HostUpdate(req):
    from updatehost import updatehost
    res=updatehost(req)
    return HttpResponse(json.dumps(res))
@Login_req
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
@Login_req
def Dasboard(req):
    from login.get_login_username import get_login_username
    username = get_login_username(req)
    from get_notin_database_ip import diff_ip
    res=diff_ip()
    try:
        obj=models.Ipnet.objects.all()
    except Exception as e:
        print(e)
    return render(req,'dashboard.html',{'pre_add_ip':res,'ipnet':obj,'cu':username,})
@Login_req
def auto_addhost(req):
    if req.method == "POST":
        from Get_Hostinfo import Get_Hostinfo
        res=Get_Hostinfo()
        print('auto')
        print(res)
        return HttpResponse(json.dumps(res))
@Login_req
def filter(req):
    if req.method == "GET":
        from login.get_login_username import get_login_username
        username = get_login_username(req)
        f_type=req.GET.get('filter_type',9999)
        f_service=req.GET.get('filter_label')
        f_service=str(f_service).encode('utf-8')
        res={'data':{'filter_type':None,'filter_service':None},'err':'0'}
        res['data']['filter_type']=int(f_type)
        res['data']['filter_service'] = f_service
        try:
            sobj = get_service_name_data()
            tobj = get_type_data()
        except Exception as e:
            print(e)
        if f_type != '9999' and f_service != '9999':
            try:
                obj1 = models.HostInfo.objects.filter(type=f_type,labels__service_name__contains=f_service)
            except Exception as e:
                print('f:')
                print(e)
            return render(req, 'hostinfo/hostlist.html',
                          {"hostlists": obj1, 'service_select': sobj, "type_select": tobj, 'cu':username,'filtervalue':res,})
        elif f_service != '9999' and f_type  == '9999':
            try:
                obj2 = models.HostInfo.objects.filter(labels__service_name__contains=f_service)
            except Exception as e:
                print('f:')
                print(e)
            return render(req, 'hostinfo/hostlist.html',
                          {"hostlists": obj2, 'service_select': sobj, "type_select": tobj, 'cu':username,'filtervalue':res,})
        elif f_service == '9999' and f_type  != '9999':
            try:
                obj3 = models.HostInfo.objects.filter(type=f_type)
            except Exception as e:
                print('f:')
                print(e)
            return render(req, 'hostinfo/hostlist.html', {"hostlists":obj3,'service_select':sobj,"type_select":tobj,'cu':username,'filtervalue':res,})
        else:
            return HttpResponseRedirect('/hostinfo/hostlist')