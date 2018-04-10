# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from newversion import  Newversion
from unfinished import Unfinished
from unfinished_detail import Unfinished_detail
# Create your views here.
def NewVersion(req):
    if req.method == 'POST':
        res=Newversion(req)
        return render(req, 'VersionIterration/newversion.html', {'msg': res})
    else:
        return render(req,'VersionIterration/newversion.html',{'msg':''})

def CheckoutUnfinished(req):
    res=Unfinished()
    return render(req,'VersionIterration/unfinished.html',{"infolist":res})
def UnfinishedDetail(req,id):
    res=Unfinished_detail(id)
    # newversiondata=res['newversion']
    # yanfadata=res['yanfa']
    # ceshidata=res['ceshi']
    # fabudata=res['fabu']
    # return render(req,'VersionIterration/unfinished_detail.html',{'newversion':newversiondata,'yanfa':yanfadata,'ceshi':ceshidata,'fabu':fabudata})
    return render(req, 'VersionIterration/unfinished_detail.html', {'data_dict':res})