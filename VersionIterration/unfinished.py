#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/10  15:00
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: unfinished.py
# @SoftWare	: PyCharm

import  models

def Unfinished():
    try:
        obj=models.NewVersion.objects.all()
    except Exception as e:
        print(e)
        return ""
    return obj