# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class HostInfo(models.Model):
    IP=models.GenericIPAddressField(primary_key=True,db_index=True)
    hostname=models.CharField(max_length=32)
    type_choices=((0,"物理宿主机"),(1,"kvm虚拟机"),(2,'docker虚拟机'),(3,"pc机"),)
    type=models.SmallIntegerField(choices=type_choices,verbose_name="主机类型",default=1)
    own_to=models.GenericIPAddressField(default=None,null=True)
    labels=models.ManyToManyField('Services')
    mem=models.CharField(max_length=16,verbose_name="总内存G")
    disk=models.CharField(max_length=64,verbose_name="磁盘情况")
    remarks=models.TextField(verbose_name="说明")
    create_time=models.DateTimeField(verbose_name="创建时间")
    destory_tiime=models.DateTimeField(verbose_name="销毁时间",null=True)

    def __str__(self):
        return "%s---%s"%(self.hostname,self.IP)
    class Meta:
        verbose_name="主机信息"
        verbose_name_plural="主机信息"

class Services(models.Model):
    tomcat_name=models.CharField(max_length=16,verbose_name="tomcat名称")
    service_name=models.CharField(max_length=16,verbose_name="项目名称")

    def __str__(self):
        return self.service_name
    class Meta:
        verbose_name="项目服务"
        verbose_name_plural="项目服务"

