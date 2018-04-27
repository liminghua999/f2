#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-25  下午3:23
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: zh.py
# @SoftWare	: PyCharm
from django import forms

class LoginForm(forms.Form):
    user = forms.CharField()
    pwd = forms.CharField()
    code = forms.CharField()
    email_code = forms.CharField()

class SendMsgForm(forms.Form):
    email = forms.CharField()