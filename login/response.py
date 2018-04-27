#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-25  下午3:22
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: response.py
# @SoftWare	: PyCharm

class StatusCodeEnum:

    Failed = 1000
    AuthFailed = 1001
    ArgsError = 1002

    Success = 2000
    # 发帖

    # 评论

    # 点赞
    FavorPlus = 2301
    FavorMinus = 2302

class BaseResponse:

    def __init__(self):
        self.status = False
        self.code = StatusCodeEnum.Success
        self.data = None
        self.summary = None
        self.message = {}