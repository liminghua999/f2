# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from sendmail.sendmail import sendMail

l=sendMail('1039976067@qq.com','665587')
l.sendmail(u='lmh')

