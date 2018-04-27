# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from response import BaseResponse
from email_random_number import random_code
from forms.zh import *
import models
from sendmail.sendmail import sendMail

def Login_req(f):
    def inner(req,*args, **kwargs):
        l = req.session.get('is_login')
        if not l :
            return HttpResponseRedirect("/")
        else:
            return f(req,*args,**kwargs)
    return inner
# Create your views here.
def Login(request):
    """
       用户登陆
       :param request:
       :return:
    """
    if request.method == "POST":
        rep = BaseResponse()
        form = LoginForm(request.POST)
        if form.is_valid():
            _value_dict = form.clean()
            if _value_dict['code'].lower() != request.session["CheckCode"].lower():
                rep.message = {'code': [{'message': '验证码错误'}]}
                return HttpResponse(json.dumps(rep.__dict__))
            # u=models.UserInfo.objects.filter(username=_value_dict['user']).values('email').distinct()

            # 验证码正确
            from django.db.models import Q
            con = Q()
            q1 = Q()
            q1.connector = 'AND'
            q1.children.append(('email', _value_dict['user']))
            q1.children.append(('password', _value_dict['pwd']))

            q2 = Q()
            q2.connector = 'AND'
            q2.children.append(('username', _value_dict['user']))
            q2.children.append(('password', _value_dict['pwd']))

            con.add(q1, 'OR')
            con.add(q2, 'OR')

            obj = models.UserInfo.objects.filter(con).first()
            if not obj:
                rep.message = {'user': [{'message': '用户名邮箱或密码错误'}]}
                return HttpResponse(json.dumps(rep.__dict__))
            u= models.UserInfo.objects.filter(username=_value_dict['user']).values('email').distinct()[0]
            c= models.SendMsg.objects.filter(email=u['email']).values('code').distinct()[0]
            if _value_dict['email_code'].lower() != c['code'].lower():
                rep.message = {'email_code': [{'message': '邮箱验证码错误'}]}
                return HttpResponse(json.dumps(rep.__dict__))
            request.session['is_login'] = True
            request.session['user_info'] = {'nid': obj.nid, 'email': obj.email, 'username': obj.username}
            rep.status = True
        else:
            error_msg = form.errors.as_json()
            rep.message = json.loads(error_msg)
        return HttpResponse(json.dumps(rep.__dict__))

    else :
        return render(request,"login/lg.html")

def LoginOut(req):
    uem=req.session['user_info']['email']
    print(uem)
    try:
        models.SendMsg.objects.filter(email=uem).delete()
        req.COOKIES.clear()
        req.session.clear()
        # del request.session['username']
        return HttpResponseRedirect('/')
    except Exception as e:
        print("删除邮箱验证码失败")
        print(e)

def send_msg(request):
    """
    登录时，发送邮箱验证码
    :param request:
    :return:
    """
    if request.method == "POST":
        rep = BaseResponse()
        form = SendMsgForm(request.POST)
        if form.is_valid():
            _value_dict = form.clean()
            email = _value_dict['email']
            has_exists_email = models.UserInfo.objects.filter(username=email).count()
            if has_exists_email:
                m= models.UserInfo.objects.filter(username=email).values("email").distinct()[0]
                print(m['email'])
                em = m['email']
                current_date = datetime.datetime.now()
                code = random_code()
                count= models.SendMsg.objects.filter(email=em).count()
                if not count:
                    models.SendMsg.objects.create(code=code, email=em, ctime=current_date)
                    rep.status = True
                    obj = sendMail(em, code)
                    obj.sendmail(u=str(email))
                else:
                    #limit_day = current_date - datetime.timedelta(hours=1)
                    limit_day = current_date - datetime.timedelta(minutes=15)
                    print("延迟时间:")
                    print(limit_day)
                    times = models.SendMsg.objects.filter(email=em, ctime__gt=limit_day, times__gt=0).count()
                    if times:
                        rep.summary = "'15分钟只允许发一次'"
                    else:
                        unfreeze = models.SendMsg.objects.filter(email=em, ctime__lt=limit_day).count()
                        if unfreeze:
                            models.SendMsg.objects.filter(email=em).update(times=0)

                        from django.db.models import F
                        obj = sendMail(em, code)
                        r = obj.sendmail(u=str(email))
                        if r:
                            models.SendMsg.objects.filter(email=em).update(code=code,
                                                                           ctime=current_date,
                                                                           times=F('times') + 1)
                            rep.status = True
                        else:
                            rep.status = False
        else:
            print('3')
            #error_dict = json.loads(form.errors.as_json())
            #rep.summary = error_dict['email'][0]['message']
            rep.summary = form.errors['email'][0]
        return HttpResponse(json.dumps(rep.__dict__))