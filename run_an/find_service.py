#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-27  下午3:17
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: find_service.py
# @SoftWare	: PyCharm

from anapi import Run_ansible
import os
from bt2.settings import BASE_DIR

FIND_SERVICE_DIR=os.path.join(BASE_DIR, 'run_an/yaml/find_service/')


def one_host(IP,ymlfilename):
    ymlfile = os.path.join(FIND_SERVICE_DIR, ymlfilename)
    pp = Run_ansible()
    pp.init_ansible()
    pp.playbook_run(ymlfile, {'Hosts': IP})
    res = pp.get_playbook_result()
    if res['ok'] != {}:
        return res['ok'][IP]
    else:
        return False

def find_java(hosts):
    return one_host(hosts,'java.yml')

def find_mysql(hosts):
    return one_host(hosts,'mysql.yml')
