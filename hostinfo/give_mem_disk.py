#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-19  下午4:58
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: give_mem_disk.py
# @SoftWare	: PyCharm

from run_an.run_shell import Get_setup_info,shell_info
updateip='192.168.0.81'
r1=shell_info(updateip,'hostname','shell')
r1.give_result()
print(r1.get_info())

r = Get_setup_info(str(updateip))
# r=shell_info(updateip,'cat /sys/class/net/vnet*/address','shell')
r.give_result()
# print(r.get_info())
n = r.hostnameinfo()
print(n)
m = r.meminfo()['total']
print(m)
d = r.diskinfo()
print(d)
