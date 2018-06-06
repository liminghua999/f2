#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time		: 18-4-25  下午3:24
# @Author	: 李明华	
# @Email	: liminghua@kangxi.info
# @File		: sendmail.py
# @SoftWare	: PyCharm

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import smtplib,os
from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
# from email import encoders
from email.header import Header
class sendMail():
    def __init__(self,to,text):
        self.to=to
        self.text=text
        self.sender = 'liminghua@kangxi.info'
        self.upass="####"
    def html(self,u):
        title = "验证码信息"
        userName = u
        t = "普通"
        captcha = self.text
        T = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title></title>
            <meta charset="utf-8" />
        </head>
        <body>
            <div class="qmbox qm_con_body_content qqmail_webmail_only" id="mailContentContainer" style="">
                <style type="text/css">
                    .qmbox body {margin: 0;padding: 0;background: #fff;font-family: "Verdana, Arial, Helvetica, sans-serif";font-size: 14px;line-height: 24px;}
                    .qmbox div, .qmbox p, .qmbox span, .qmbox img {margin: 0;padding: 0;}
                    .qmbox img {border: none; }
                    .qmbox .contaner {margin: 0 auto;}
                    .qmbox .title {margin: 0 auto;background: url() #CCC repeat-x;height: 30px;text-align: center;font-weight: bold;padding-top: 12px;font-size: 16px;}
                    .qmbox .content {margin: 4px;}
                    .qmbox .biaoti {padding: 6px;color: #000;}
                    .qmbox .xtop, .qmbox .xbottom {display: block;font-size: 1px;}
                    .qmbox .xb1, .qmbox .xb2, .qmbox .xb3, .qmbox .xb4 {display: block;overflow: hidden;}
                    .qmbox .xb1, .qmbox .xb2, .qmbox .xb3 {height: 1px;}
                    .qmbox .xb2, .qmbox .xb3, .qmbox .xb4 {border-left: 1px solid #BCBCBC;border-right: 1px solid #BCBCBC;}
                    .qmbox .xb1 {margin: 0 5px;background: #BCBCBC;}
                    .qmbox .xb2 {margin: 0 3px;border-width: 0 2px;}
                    .qmbox .xb3 {margin: 0 2px;}
                    .qmbox .xb4 {height: 2px;margin: 0 1px;}
                    .qmbox .xboxcontent {display: block;border: 0 solid #BCBCBC;border-width: 0 1px;}
                    .qmbox .line {margin-top: 6px;border-top: 1px dashed #B9B9B9;padding: 4px;}
                    .qmbox .neirong {padding: 6px;color: #666666;}
                    .qmbox .foot {padding: 6px;color: #777;}
                    .qmbox .font_darkblue {color: #006699;font-weight: bold;}
                    .qmbox .font_lightblue {color: #008BD1;font-weight: bold;}
                    .qmbox .font_gray {color: #888;font-size: 12px;}
                </style>
                <div class="contaner">
                    <div class="title">%s</div>
                    <div class="content">
                        <p class="biaoti"><b>亲爱的用户，你好！</b></p>
                        <b class="xtop"><b class="xb1"></b><b class="xb2"></b><b class="xb3"></b><b class="xb4"></b></b>
                        <div class="xboxcontent">
                            <div class="neirong">
                                <p><b>请核对你的用户名：</b><span id="userName" class="font_darkblue">%s</span></p>
                                <p><b>%s的验证码：</b><span class="font_lightblue"><span id="yzm" data=%s onclick="return false;" t="7" style="border-bottom: 1px dashed rgb(204, 204, 204); z-index: 1; position: static;">%s</span></span><br><span class="font_gray">(请输入该验证码完成%s，验证码15分钟内有效！)</span></p>
                            </div>
                        </div>
                        <b class="xbottom"><b class="xb4"></b><b class="xb3"></b><b class="xb2"></b><b class="xb1"></b></b>
                    </div>
                </div>
                <style type="text/css">
                    .qmbox style, .qmbox script, .qmbox head, .qmbox link, .qmbox meta {
                        display: none !important;
                    }
                </style>
            </div>
        </body>
        </html>
        """ % (title, userName,userName , captcha, captcha, t)
        return T
    def attach(self,path,info):
        filepath = path
        msg=info
        r = os.path.exists(filepath)
        # if r is False:
        #     msg.attach(MIMEText('no file...', 'plain', 'utf-8'))
        # else:
        #     # 邮件正文是MIMEText:
        #     msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
            # 遍历指定目录，显示目录下的所有文件名
        pathDir = os.listdir(filepath)
        for allDir in pathDir:
            child = os.path.join(filepath, allDir)
            print child.decode('gbk')  # .decode('gbk')是解决中文显示乱码问题
            with open(child, 'rb') as f:
                # mime = MIMEBase('file', 'xls', filename=allDir)
                mime = MIMEText(f.read(),'base64','gbk')
                mime["Content-Type"] = 'application/octet-stream'
                # 加上必要的头信息:
                mime.add_header('Content-Disposition', 'attachment', filename=('gbk', '',allDir))
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                #mime.set_payload(f.read())
                # 用Base64编码:
                #encoders.encode_base64(mime)
                # return mime
                msg.attach(mime)
    def sendmail(self,path=None,u=None):
        T=self.html(u=u)
        ret = 1
        try:
            msg = MIMEText(T, 'html','utf-8')
            info = MIMEMultipart()
            info.attach(msg)  # 添加到MIMEMultipart:
            info['From'] = formataddr([Header("李", 'utf-8').encode(), self.sender])
            info['To'] =  self.to
            #info['To'] = ",".join(self.to)
            info['Subject'] = Header("测试使用",'utf-8')
            if path != None:
                self.attach(path,info) # 添加到MIMEMultipart:
                # info.attach(M)
            server = smtplib.SMTP("smtp.exmail.qq.com", 25)
            server.set_debuglevel(1)
            server.login(self.sender, self.upass)
            server.sendmail(self.sender, [self.to,], info.as_string())
            server.quit()
        except Exception as e:
            print(e)
            ret = 0
        return ret

