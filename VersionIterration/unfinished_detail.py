#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/10  15:50
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: unfinished_detail.py
# @SoftWare	: PyCharm
from VersionIterration import models
def Unfinished_detail(id):
    data={'newversion':None,'yanfa':None,'ceshi':None,'fabu':None}
    try:
        newversion_obj=models.NewVersion.objects.filter(id=id)[0]
    except Exception as e:
        print(e)
        return '查询发起版本信息失败!!,请重试！'
    data['newversion']=newversion_obj
    try:
        yanfaobj=models.Development.objects.filter(newversionid=newversion_obj.id)
    except Exception as e:
        return "查询开发信息失败！请重试"
    if yanfaobj.exists():
        try:
            ceshiobj = models.TestContent.objects.filter(newversionid=newversion_obj.id)
        except Exception as e:
            return "查询测试信息失败！请重试"
        if ceshiobj.exists():
            try:
                fabuobj = models.UpdateVersion.objects.filter(newversionid=newversion_obj.id)
            except Exception as e:
                return "查询发布信息失败！请重试"
            data['fabu']=fabuobj
        data['ceshi']=ceshiobj
    data['yanfa']=yanfaobj
    return data


