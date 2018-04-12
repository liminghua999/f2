#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 2018/4/11  9:58
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: unfinished_continue.py
# @SoftWare	: PyCharm
import logging
logging.getLogger('django')
import  models
from hostinfo import models as hostmodels

def get_newversion_data(id):
    try:
        obj=models.NewVersion.objects.filter(id=id)[0]
    except Exception as e:
        logging.error(e)
        logging.error('获取发起版本信息失败')
        obj=False
    return obj

def yanfa(req,id):
    res='0'
    yoperateman=req.POST.get('yoperateman')
    yinform_nextman=req.POST.get('yinform_nextman')
    apinum=int(req.POST.get('apinum'))
    apilist=[]
    for num in range(apinum):
        apiid='yapi'+str(num+1)
        apilist.append(str(req.POST.get(apiid)))
    if yoperateman and yinform_nextman and apinum:
        try:
            yanfaobj=models.Development.objects.create(operate_username=yoperateman,inform_nextman=yinform_nextman,newversionid=id)
        except Exception as e:
            logging.error(e)
            logging.error('写入开发操作失败，请重试！！')
            res="操作失败，请重试！！"
            return  res
        try:
            projectname=models.NewVersion.objects.filter(id=id)[0]
            print(projectname.project_name)
            for oneapi in apilist:
                oneapidata=oneapi.split()
                apiurl=oneapidata[0]
                print(apiurl)
                apiintroduce=oneapidata[1]
                print(apiintroduce)
                apiobj=models.Api.objects.create(project_name=projectname.project_name,api_name=apiurl,api_introduce=apiintroduce)
                yanfaobj.update_version_newapi.add(apiobj.id)
                yanfaobj.save()
        except Exception as e:
            logging.error(e)
            logging.error('api数据写入失败')
            res="api数据写入失败"
            return res
        return res
    else:
        res="有选项未填写！！"
        return res

def ceshi(req,id):
    res = '0'
    coperateman = req.POST.get('coperateman')
    cinform_nextman = req.POST.get('cinform_nextman')
    testcontentnum = int(req.POST.get('testcontentnum'))
    testcontentlist = []
    for num in range(testcontentnum):
        ctestid = 'ctest' + str(num + 1)
        testcontentlist.append(str(req.POST.get(ctestid)))
    if coperateman and cinform_nextman:
        try:
            ceshiobj = models.Test.objects.create(operate_username=coperateman, inform_nextman=cinform_nextman,
                                                         newversionid=id)
        except Exception as e:
            logging.error(e)
            logging.error('创建测试的数据失败')
            res = "操作失败，请重试！！"
            return res
        try:
            projectname = models.NewVersion.objects.filter(id=id)[0]
            print(projectname.project_name)
            for onecontent in testcontentlist:
                onecontentdata = onecontent.split()
                testcontent = onecontentdata[0]
                print(testcontent)
                teststatus = onecontentdata[1]
                print(teststatus)
                testcontentobj = models.TestContent.objects.create(project_name=projectname.project_name, content=testcontent,
                                                   status=teststatus)
                ceshiobj.test_content.add(testcontentobj.id)
                ceshiobj.save()
        except Exception as e:
            logging.error(e)
            logging.error('创建测试内容的数据失败')
            res = "测试内容数据写入失败"
            return res
        return res
    else:
        res = "有选项未填写！！"
        return res

def fabup(req,id):
    pass
def get_project_host(projectname):
    try:
        serviceobj=hostmodels.Services.objects.filter(service_name=projectname)[0]
    except Exception as e:
        logging.error(e)
        logging.error('获取服务的信息失败')
    try:
        hostobj=serviceobj.hostinfo_set.all()
    except Exception as e:
        logging.error(e)
        logging.error('获取和服务相关联的主机信息失败')
    res=[]
    for host in hostobj:
        res.append(host.IP)
    return res
