#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/10  13:51
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: newversion.py
# @SoftWare	: PyCharm

import models

def Newversion(req):
    gstartman=req.POST.get('startman')
    gproject_name=req.POST.get('projectname')
    gproject_version = req.POST.get('projectversion')
    gupdatecontent = req.POST.get('updatecontent')
    ginform_nextman = req.POST.get('inform_nextman')
    print(gstartman,gproject_name,gproject_version,gupdatecontent,ginform_nextman)
    if gstartman and gproject_version and gproject_name and gupdatecontent and ginform_nextman:
        try:
            models.NewVersion.objects.create(start_username=gstartman,project_name=gproject_name,project_version=gproject_version,
                                                 update_content=gupdatecontent,inform_nextman=ginform_nextman)
        except Exception as e:
            print(e)
            return "发起失败，请重试"
        return  "发起完成！！"
    else:
        return "有未填写选项，请填写！！"
