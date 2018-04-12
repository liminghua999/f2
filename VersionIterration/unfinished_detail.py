#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/10  15:50
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: unfinished_detail.py
# @SoftWare	: PyCharm

import logging
logging.getLogger('django')
from VersionIterration import models
def Unfinished_detail(id):
    data={'newversion':None,'yanfa':None,'ceshi':None,'fabu':None}
    try:
        newversion_obj=models.NewVersion.objects.filter(id=id)[0]
    except Exception as e:
        logging.error(e)
        logging.error('查询发起版本信息失败!!,请重试！')
        return '查询发起版本信息失败!!,请重试！'
    data['newversion']=newversion_obj
    try:
        yanfaobj=models.Development.objects.filter(newversionid=newversion_obj.id)
    except Exception as e:
        logging.error(e)
        logging.error('查询开发信息失败!!,请重试！')
        return "查询开发信息失败！请重试"
    if yanfaobj.exists():
        try:
            ceshiobj = models.Test.objects.filter(newversionid=newversion_obj.id)
        except Exception as e:
            logging.error(e)
            logging.error('查询测试信息失败!!,请重试！')
            return "查询测试信息失败！请重试"
        if ceshiobj.exists():
            try:
                fabuobj = models.UpdateVersion.objects.filter(newversionid=newversion_obj.id)
            except Exception as e:
                logging.error(e)
                logging.error('查询发布信息失败!!,请重试！')
                return "查询发布信息失败！请重试"
            if fabuobj.exists():
                data['fabu']=fabuobj[0]
            data['ceshi']=ceshiobj[0]
        data['yanfa']=yanfaobj[0]
    return data


