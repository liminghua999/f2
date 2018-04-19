#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-19  下午4:58
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: mem_disk.py
# @SoftWare	: PyCharm
import models
from run_an.run_shell import Get_setup_info
from hostinfo.addhost import disk_add
def mem_disk(listip):
    for ip in listip:
        try:
            print('7')
            obj=models.HostInfo.objects.filter(IP=ip)
        except Exception as e:
            print(e)
        if obj:
            data = Get_setup_info(ip)
            data.give_result()
            n = data.hostnameinfo()
            m = data.meminfo()['total']
            d = data.diskinfo()
            did = disk_add(d)
            if did:
                print('8')
                try:
                    obj.update(hostname=n,mem=m)
                    for tid in did:
                        obj.disk.add(tid)
                    obj.save()
                except Exception as e:
                    print("更新mem disk hostname信息失败")
                    print(e)