#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-19  上午11:26
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: get_hostinfo.py
# @SoftWare	: PyCharm
import nmap
def get_hostinfo():
    nmpobj = nmap.PortScanner()
    obj = nmpobj.scan(hosts='192.168.0.0/24', arguments="-n -sP -PE")
    all = obj['scan']
    for i in all:
        # print(all[i]['vendor'].values())
        if 'QEMU Virtual NIC' in all[i]['vendor'].values():
            # print(i)
            pass
        else:
            print(all[i]['vendor'])
get_hostinfo()
