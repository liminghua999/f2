# -*- coding: utf-8 -*-
from django.http import HttpResponse

from hostinfo import models
import json
from run_an.run_shell import Get_setup_info


def host_add(req):
    if req.method == "POST":
        rt = {'data': None, 'err': '0'}
        print(req.POST)
        hip = req.POST.get('ip')
        htype = req.POST.get('type')
        hlabels = str(req.POST.get('labels')).split()
        hgip = req.POST.get('gip')
        hctime = req.POST.get('ctime')
        print(hgip)
        print(hctime)
        if hip != None:
            s = models.HostInfo.objects.filter(IP=hip).count()
            if s:
                print("IP:")
                rt['err'] = "IP:存在"
                return HttpResponse(json.dumps(rt))
            else:
                data = Get_setup_info(hip)
                data.give_result()
                n = data.hostnameinfo()
                m = data.meminfo()['total']
                d = data.diskinfo()
                try:
                    obj=models.HostInfo.objects.create(IP=hip, type=htype,own_to=hgip,create_time=hctime,
                                                   hostname=n,mem=m, disk=d)
                    for lb in hlabels:
                        print(models.Services.objects.filter(service_name__contains=lb).only('id')[0])
                        obj.labels.add(models.Services.objects.filter(service_name__contains=lb).only('id')[0])
                    obj.save()
                except Exception as e:
                    rt['err'] = "添加主机信息失败"
                    print("更新主机信息失败")
                    print(e)
                    return rt
                try:
                    obj = models.HostInfo.objects.filter(IP=hip)
                except Exception as e:
                    rt['err'] = "获取主机信息失败"
                    return rt
                d = {'ip': None, 'hostname': None, 'labels': None, 'type': None, 'mem': None, 'disk': None,
                     'remarks': None,'own_to':None,'ctime':None,'dtime':None}
                for i in obj:
                    d['ip'] = i.IP
                    d['hostname'] = i.hostname
                    lab=""
                    for j in i.labels.all():
                        tmp="""<span>%s-%s</span><br>"""%(j.service_name,j.tomcat_name)
                        lab=lab+tmp
                    d['labels'] = lab
                    d['type'] = i.get_type_display()
                    d['mem'] = i.mem
                    d['disk'] = i.disk
                    d['remarks'] = i.remarks
                    d['own_to'] = i.own_to
                    d['ctime'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                    d['dtime'] = i.destory_tiime
                rt['data'] = d
                return rt
        else:
            rt['err']="IP is null!!"
            return rt