#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/18  16:48
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: get_online_ip.py
# @SoftWare	: PyCharm

import logging

logging.getLogger('django')

import  nmap,yaml,os
def get_online_ip():
    d=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.yaml')
    with open(d,'rb') as f:
        ymobj=yaml.load(f)
        ipnets=ymobj['hostinfo']['ipnet']
    res={}
    for ipnet in ipnets:
        res[ipnet]={}
        nmpobj = nmap.PortScanner()
        all=nmpobj.scan(hosts=ipnet,arguments="-n -sP -PE")
        ip_all_num=all['nmap']['scanstats']['totalhosts']
        res[ipnet]['ip_all_num']=ip_all_num
        ip_used_num=all['nmap']['scanstats']['uphosts']
        res[ipnet]['ip_used_num']=ip_used_num
        ip_free_num=all['nmap']['scanstats']['downhosts']
        res[ipnet]['ip_free_num']=ip_free_num
        all_online_ip=nmpobj.all_hosts()
        res[ipnet]['ip_used']=all_online_ip
        return res
# get_online_ip()
