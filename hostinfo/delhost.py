# -*- coding: utf-8 -*-
import models

def DelHost(req):
    res='0'
    if req.method == "POST":
        hdel_ip = req.POST.get('del_ip',0)
        if hdel_ip:
            try:
                obj=models.HostInfo.objects.filter(IP=hdel_ip)[0]
            except Exception as e:
                print(e)
                res = "查询删除IP出错，请重试!"
                return res
            for d in obj.disk.all():
                obj.disk.remove(d.id)
                # models.DiskInfo.objects.filter(id=d.id).delete()
                d.delete()
            for l in obj.labels.all():
                obj.labels.remove(l.id)
            obj.delete()
        return res
