#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/18  16:48
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: get_online_ip.py
# @SoftWare	: PyCharm

import logging

logging.getLogger('django')

import  nmap,yaml,os,json

def get_online_ip():
    d=os.path.join(os.path.dirname(os.path.abspath(__file__)),'conf.yaml')
    with open(d,'rb') as f:
        ymobj=yaml.load(f)
        ipnet=ymobj['hostinfo']['ipnet']
    nmpobj=nmap.PortScanner()
    nmpobj.all_hosts()
    print(nmpobj)
get_online_ip()
