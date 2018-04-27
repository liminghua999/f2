#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-25  下午3:11
# @Author	: 李明华
# @Email	: liminghua@kangxi.info
# @File		: yanzhengma.py
# @SoftWare	: PyCharm

import io
import check_code as CheckCode
from django.shortcuts import HttpResponse
def check_code(request):
    """
    获取验证码
    :param request:
    :return:
    """
    stream = io.BytesIO()
    # 创建随机字符 code
    # 创建一张图片格式的字符串，将随机字符串写到图片上
    img, code = CheckCode.create_validate_code()
    img.save(stream, "PNG")
    # 将字符串形式的验证码放在Session中
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())
