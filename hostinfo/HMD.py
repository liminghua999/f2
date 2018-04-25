#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-23  下午4:42
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: HMD.py
# @SoftWare	: PyCharm

import models
from run_an.run_shell import Get_setup_info,ops_ip
from hostinfo.addhost import disk_add
def HMD(listip):
    print(listip)
    for updateip in listip:
        try:
            obj=models.HostInfo.objects.filter(IP=updateip)
        except Exception as e:
            print(e)
        if obj.exists():
            print(updateip)
            try:
                check_ip = ops_ip(updateip)
                if not check_ip.check_ip():
                    check_ip.add_ip()

                r = Get_setup_info(str(updateip))
                r.give_result()
                n = r.hostnameinfo()
                print(n)
                m = r.meminfo()['total']
                d = r.diskinfo()
                did = disk_add(d)
                if did:
                    try:
                        obj.update(hostname=n,mem=m)
                        for tid in did:
                            obj[0].disk.add(tid)
                        obj[0].save()
                    except Exception as e:
                        print("更新mem disk hostname信息失败")
                        print(e)
            except Exception as e:
                print(updateip+'run_an failed')
                print(e)
        else:
            print('obj not exists')