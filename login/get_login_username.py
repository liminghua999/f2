#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-25  下午3:58
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: get_login_username.py
# @SoftWare	: PyCharm

def get_login_username(req):
    l = req.session.get('user_info')
    return l['username']
