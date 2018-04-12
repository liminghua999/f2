# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse
from newversion import  Newversion
from unfinished import Unfinished
from unfinished_detail import Unfinished_detail
from unfinished_continue import *
import json
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
    return render(req, 'VersionIterration/unfinished_detail.html', {'data_dict':res})

def UnfinishedContinue(req,id,part):
    if req.method == 'POST':
        if str(part) == 'yanfa':
            res=yanfa(req,id)
            return HttpResponse(json.dumps(res))
        elif str(part) == 'ceshi':
            res=ceshi(req,id)
            return HttpResponse(json.dumps(res))
        else:
            pass
    else:
        if str(part) == 'fabu':
            versiondata=get_newversion_data(id)
            hostlist=get_project_host(versiondata.project_name)
            print(hostlist)
            return render(req,'VersionIterration/unfinished_continue_fabu.html',{'versiondata':versiondata,'hostlist':hostlist})