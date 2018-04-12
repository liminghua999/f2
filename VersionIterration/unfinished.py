#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/10  15:00
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: unfinished.py
# @SoftWare	: PyCharm
import  logging
logging.getLogger('django')
import  models

def Unfinished():
    try:
        obj=models.NewVersion.objects.all()
    except Exception as e:
        logging.error(e)
        logging.error('创建测试的数据失败')
        return ""
    return obj