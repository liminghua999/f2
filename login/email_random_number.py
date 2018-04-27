#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-25  下午3:22
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: email_random_number.py
# @SoftWare	: PyCharm
import random
def random_code():
    code = ''
    for i in range(4):
        current = random.randrange(0,4)
        if current != i:
            temp = chr(random.randint(65,90))
        else:
            temp = random.randint(0,9)
        code += str(temp)
    return code