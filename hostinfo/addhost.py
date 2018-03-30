from django.http import HttpResponse

from hostinfo import models
import json

def host_add(req):
    if req.method == "POST":
        rt={'data':None,'err':None}
        hip=req.POST.get('ip')
        print(hip)
        htype=req.POST.get('type')
        hlabels=req.POST.get('labels')
        s= models.HostList.objects.filter(ip=hip).count()
        if  s:
           print("IP存在")
           rt['err'] ="IP存在"
           return HttpResponse(json.loads(rt))
        else:
            try:
                models.HostList.objects.create(ip=hip, type=htype, labels=hlabels)
            except Exception as e:
                rt['err']='添加主机失败'
                print(e)
                return HttpResponse(json.loads(rt))
            ncmd="ansible %s -m shell -a 'hostname' | grep -v %s"%(hip,hip)
            hhostname=Shell(ncmd)
            n=hhostname.exe_bash()
            mcmd="ansible %s -m shell -a 'free -m' | grep -v %s"%(hip,hip)
            hmem=Shell(mcmd)
            m=hmem.exe_bash()
            dcmd="ansible %s -m shell -a 'df -h' | grep -v %s"%(hip,hip)
            hdisk=Shell(dcmd)
            d=hdisk.exe_bash()
            rt['data']= models.HostList.objects.filter(ip=hip)
            return HttpResponse(json.loads(rt))