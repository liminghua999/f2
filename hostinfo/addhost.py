# -*- coding: utf-8 -*-
from django.http import HttpResponse

from hostinfo import models
import json
from run_an.run_shell import Get_setup_info

def disk_add(data):
    print(data)
    print(type(data))
    tmp = []
    for option in data:
        for i in option:
            print(i)
            print(option[i]['total'])
        try:
            obj=models.DiskInfo.objects.create(mount_name=i,mount_size=option[i]['total'])
        except Exception as e:
            print("disk:")
            print(e)
            return False
        tmp.append(obj.id)
    return tmp
def host_add(req):
    if req.method == "POST":
        rt = {'data': None, 'err': '0'}
        print(req.POST)
        hip = req.POST.get('ip')
        htype = int(req.POST.get('type'))-1
        hlabels = str(req.POST.get('labels')).split()
        # hlabels =req.POST.getlist('labels')
        print(hlabels)
        hgip = req.POST.get('gip')
        hctime = req.POST.get('ctime')
        if hip != None:
            s = models.HostInfo.objects.filter(IP=hip).count()
            if s:
                print("IP:")
                rt['err'] = "IP存在"
                return rt
            else:
                data = Get_setup_info(hip)
                data.give_result()
                n = data.hostnameinfo()
                m = data.meminfo()['total']
                d = data.diskinfo()
                did=disk_add(d)
                print(did)
                if did:
                    try:
                        obj=models.HostInfo.objects.create(IP=hip, type=htype,own_to=hgip,create_time=hctime,
                                                       hostname=n,mem=m)
                        for lb in hlabels:
                            obj.labels.add(models.Services.objects.filter(service_name__contains=lb).only('id')[0])
                        for tid in did:
                            obj.disk.add(tid)
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
                    rdata = {'ip': None, 'hostname': None, 'labels': None, 'type': None, 'mem': None, 'disk': None,
                         'remarks': None,'own_to':None,'ctime':None,'dtime':None}
                    for i in obj:
                        rdata['ip'] = i.IP
                        rdata['hostname'] = i.hostname
                        lab=""
                        for j in i.labels.all():
                            tmp="""<span>%s-%s</span><br>"""%(j.service_name,j.tomcat_name)
                            lab=lab+tmp
                        rdata['labels'] = lab
                        rdata['type'] = i.get_type_display()
                        rdata['mem'] = i.mem
                        di=""
                        for dd in i.disk.all():
                            dtmp="""<span class="row" style="margin: 0;"><span class="col-sm-4 col-sm-offset-2"><b>%s</b></span><span class="col-sm-1">%s</span></span>"""%(dd.mount_name,dd.mount_size)
                            di+=dtmp
                        rdata['disk'] = di
                        rdata['remarks'] = i.remarks
                        rdata['own_to'] = i.own_to
                        rdata['ctime'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                        rdata['dtime'] = i.destory_tiime
                    rt['data'] = rdata
                    return rt
        else:
            rt['err']="IP is null!!"
            return rt