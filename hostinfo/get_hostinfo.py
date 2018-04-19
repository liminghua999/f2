#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-19  上午11:26
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: get_hostinfo.py
# @SoftWare	: PyCharm
import nmap,models
from hostinfo.get_notin_database_ip import diff_ip
from hostinfo.mem_disk import mem_disk
from hostinfo.own_to import own_to
def get_hostinfo():
    res=diff_ip()
    nmpobj = nmap.PortScanner()
    obj = nmpobj.scan(hosts='192.168.0.0/24', arguments="-n -sP -PE")
    all = obj['scan']
    for i in all:
        if i in res:
            if 'QEMU Virtual NIC' in all[i]['vendor'].values():
                try:
                    print('1')
                    models.HostInfo.objects.create(IP=i,mac=all[i]['addresses']['mac'],type=1)
                except Exception as e:
                    print('2')
                    print(e)
            else:
                onehost=nmpobj.scan(hosts=i, arguments="-n -PE")
                flag=1
                print('3')
                for service in onehost['scan'][i]['tcp']:
                    if  onehost['scan'][i]['tcp'][service]['name'] == "ssh":
                        print('4')
                        flag=0
                        try:
                            models.HostInfo.objects.create(IP=i, mac=all[i]['addresses']['mac'], type=0)
                        except Exception as e:
                            print(e)
                        break
                if flag:
                    try:
                        models.HostInfo.objects.create(IP=i, mac=all[i]['addresses']['mac'], type=3)
                    except Exception as e:
                        print(e)
    print('5')
    mem_disk(res)
    print('6')
    own_to()
    return 1

# get_hostinfo()
