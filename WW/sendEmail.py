#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
"""
sender = 'shunhu'
receiver = '1670057209@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEMultipart('alternative')
textplain = MIMEText('【顺呼】您正在重置您的密码，这是您的验证码', _subtype='plain', _charset='UTF-8')
texthtml = MIMEText('您正在重置的密码,您的验证码是:【%s】，请不要透露给他人。如非本人操作，请忽略。验证码有效时长30分钟。', _subtype='html', _charset='UTF-8')
message.attach(textplain)
message.attach(texthtml)
message['From'] = Header("admin@lastation.me")   # 发送者
message['To'] = receiver        # 接收者
 
subject = '您正在修改密码'
message['Subject'] = Header(subject, 'utf-8')
 
 
try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receiver, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
"""

def sendVeriEmail(receiver, veri_code):
    sender = 'shunhu'
    message = MIMEMultipart('alternative')
    textplain = MIMEText('【顺呼】您正在重置您的密码，这是您的验证码', _subtype='plain', _charset='UTF-8')
    texthtml = MIMEText('您正在重置的密码,您的验证码是:【%s】，请不要透露给他人。如非本人操作，请忽略。验证码有效时长30分钟。' % veri_code, _subtype='html', _charset='UTF-8')
    message.attach(textplain)
    message.attach(texthtml)
    message['From'] = Header("admin@lastation.me")   # 发送者
    message['To'] = receiver        # 接收者
    
    subject = '您正在修改密码'
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
