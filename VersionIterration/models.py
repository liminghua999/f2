# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from hostinfo.models import Services

# Create your models here.
class NewVersion(models.Model):
    login_username=models.CharField(max_length=16,verbose_name="登录的用户")
    start_username=models.ForeignKey('OperateMan',verbose_name="发起人")
    project_name=models.ForeignKey('Services',verbose_name="项目名称")
    update_content = models.TextField(verbose_name='本次版本迭代的主要内容')
    start_time = models.DateTimeField(auto_now_add=True)
    inform_nextman = models.ForeignKey('OperateMan',verbose_name="被通知的下一位操作人")

    def __str__(self):
        return '%s发起%s版本迭代'%(self.start_username,self.project_name)
    class Meta():
        verbose_name="版本迭代"
        verbose_name_plural="版本迭代"

class OperateMan(models.Model):
    name=models.CharField(max_length=16,verbose_name="名字")
    email=models.EmailField(verbose_name="邮箱")
    type_choices=({'1':'产品'},{'2':'研发'},{'3':'测试'},{'4':'运维'},{'5','运营'})
    type=models.CharField(choices=type_choices,verbose_name='角色')
    def __str__(self):
        return '%s-%s'%(self.get_type_display(),self.name)
    class Meta():
        verbose_name = "操作人"
        verbose_name_plural = "操作人"

class Development(models.Model):
    operate_username = models.ForeignKey('OperateMan', verbose_name="操作人")
    update_version_newapi = models.ForeignKey('Api',verbose_name='本次新增接口')
    def __str__(self):
        return '研发-%s-新增接口'%self.operate_username

class Api(models.Model):
    project_name=models.ForeignKey('Services',verbose_name='归属项目名称')
    api_name=models.CharField(max_length=64,verbose_name='接口url')

