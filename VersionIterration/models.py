# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class OperateMan(models.Model):
    name=models.CharField(max_length=16,verbose_name="名字")
    email=models.EmailField(verbose_name="邮箱")
    type_choices=(('1','产品'),('2','研发'),('3','测试'),('4','运维'),('5','运营'))
    type=models.CharField(max_length=2,choices=type_choices,verbose_name='角色')
    def __str__(self):
        return '%s-%s'%(self.get_type_display(),self.name)
    class Meta:
        verbose_name = "操作人"
        verbose_name_plural = "操作人"

class NewVersion(models.Model):
    login_username=models.CharField(max_length=16,verbose_name="登录的用户")
    start_username=models.CharField(max_length=16,verbose_name="发起人")
    project_name=models.CharField(max_length=16,verbose_name="项目名称")
    project_version=models.CharField(max_length=8,verbose_name="项目版本",default='v1.0')
    update_content = models.TextField(verbose_name='本次版本迭代的主要内容')
    operate_time = models.DateTimeField(auto_now_add=True)
    inform_nextman = models.CharField(max_length=16,verbose_name="被通知的下一位操作人")
    status=models.BooleanField(default=False,verbose_name="版本迭代最终状态")

    def __str__(self):
        return '%s发起%s版本迭代'%(self.start_username,self.project_name)
    class Meta:
        verbose_name="版本迭代"
        verbose_name_plural="版本迭代"

class Development(models.Model):
    login_username = models.CharField(max_length=16, verbose_name="登录的用户")
    operate_username = models.CharField(max_length=16, verbose_name="操作人")
    update_version_newapi = models.ManyToManyField('Api',verbose_name='本次新增接口')
    inform_nextman = models.CharField(max_length=16, verbose_name="被通知的下一位操作人",default='测试1')
    operate_time = models.DateTimeField(auto_now_add=True)
    newversionid=models.CharField(max_length=8, verbose_name="更新项目的编号",default=0)

    def __str__(self):
        return '研发-%s-新增接口'%self.operate_username
    class Meta:
        verbose_name="研发情况"
        verbose_name_plural="研发情况"

class Api(models.Model):
    project_name=models.CharField(max_length=16,verbose_name='归属项目名称')
    api_name=models.CharField(max_length=64,verbose_name='接口url')
    api_introduce=models.CharField(max_length=64,verbose_name='接口说明',default=None)

class Test(models.Model):
    operate_username = models.CharField(max_length=16, verbose_name="操作人")
    test_content=models.ManyToManyField('TestContent',verbose_name='测试的功能')
    operate_time = models.DateTimeField(auto_now_add=True)
    inform_nextman = models.CharField(max_length=16, verbose_name="被通知的下一位操作人",default='运维1')
    newversionid = models.CharField(max_length=8, verbose_name="更新项目的编号",default=0)
    class Meta:
        verbose_name="测试情况"
        verbose_name_plural="测试情况"

class TestContent(models.Model):
    project_name = models.CharField(max_length=16, verbose_name='归属项目名称')
    content=models.CharField(max_length=64,verbose_name="测试的功能")
    status_choices=(('0','失败'),('1','成功'))
    status=models.CharField(choices=status_choices,verbose_name="测试结果的状态",max_length=2)

class UpdateVersion(models.Model):
    project_name = models.CharField(max_length=16, verbose_name='归属项目名称')
    operate_username = models.CharField(max_length=16, verbose_name="操作人")
    operate_time = models.DateTimeField(auto_now_add=True)
    get_code_choices=(('1','git'),('2','svn'),('3','上传文件'))
    get_code_type=models.CharField(choices=get_code_choices,verbose_name="获取代码的方式",max_length=2)
    get_code_url=models.URLField(verbose_name="获取代码的地址")
    newversionid = models.CharField(max_length=8, verbose_name="更新项目的编号",default=0)
    def __str__(self):
        return "%s于%s版本更新"%(self.project_name,self.operate_time)
    class Meta:
        verbose_name='版本更新'
        verbose_name_plural='版本更新'
