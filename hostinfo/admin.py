# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from hostinfo import models
import sys
reload(sys)

sys.setdefaultencoding('utf8')

# Register your models here.

admin.site.register(models.HostInfo)
admin.site.register(models.Services)