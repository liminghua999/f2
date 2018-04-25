#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-19  上午11:26
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: Get_Hostinfo.py
# @SoftWare	: PyCharm
import nmap,models
from hostinfo.get_notin_database_ip import diff_ip
from hostinfo.HMD import HMD
from hostinfo.own_to import own_to
def Get_Hostinfo():
    res=diff_ip()
    sship=[]
    nmpobj = nmap.PortScanner()
    obj = nmpobj.scan(hosts='192.168.0.0/24', arguments="-n -sP -PE")
    all = obj['scan']
    for i in all:
        t=-1
        if i in res:
            if 'QEMU Virtual NIC' in all[i]['vendor'].values():
                t=1
                sship.append(i)
            else:
                onehost=nmpobj.scan(hosts=i, arguments="-n -PE")
                if 'tcp' in onehost['scan'][i]:
                    flag=1
                    for service in onehost['scan'][i]['tcp']:
                        if  onehost['scan'][i]['tcp'][service]['name'] == "ssh":
                            sship.append(i)
                            flag=0
                            t=0
                            break

                        if 'microsoft' in onehost['scan'][i]['tcp'][service]['name']:
                            flag=0
                            t=3
                            break
                    if flag:
                        t=4
                else:
                    print(i+"no tcp item")
                    t=999
            if 'mac' in all[i]['addresses']:
                Mac=all[i]['addresses']['mac']
            else:
                print(i + 'no mac')
                Mac=''
            if t != 999:
                try:
                    models.HostInfo.objects.create(IP=i, mac=Mac, type=t)
                except Exception as e:
                    print('add failed')
                    print(e)

    if sship.__len__():
        HMD(sship)
        own_to()
    return 1

