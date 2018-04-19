#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-18  下午5:58
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: get_notin_database_ip.py
# @SoftWare	: PyCharm

from hostinfo.get_online_ip import get_online_ip
import models
def diff_ip():
    res=get_online_ip()
    for net in res:
        try:
            models.Ipnet.objects.create(ipnet=net, ip_all_num=res[net]['ip_all_num'], ip_free_num=res[net]['ip_free_num'], ip_used_num=res[net]['ip_used_num'])
        except Exception as e:
            print(e)
    try:
        database_ip_obj=models.HostInfo.objects.values_list('IP',flat=True)
    except Exception as e:
        print(e)
    database_ip=[]
    for i in database_ip_obj:
        database_ip.append(i)
    pre_add_ip=list(set(res[net]['ip_used'])^set(database_ip))
    return pre_add_ip

# diff_ip()