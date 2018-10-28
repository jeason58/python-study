#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xlrd
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 收件人信息文件名
filename = "./files/test.xls"


# 获取收件人列表
def get_receivers():
    book = xlrd.open_workbook(filename=filename)
    sheet = book.sheet_by_index(0)
    mail_list = []
    for i in range(1, sheet.nrows):
        address = "".join(sheet.cell(i, 12).value).strip()
        mail_list.append(address)
    return mail_list


# 邮件相关配置参数
_Host = "smtp.qq.com"  # 发件人邮箱服务器地址
_Port = 25  # 邮箱服务器端口
_User = "sender@qq.com"  # 发件人邮箱地址
_Pwd = "your_password"  # 发件人邮箱密码
_From = _User
# _To_List = get_receivers()   # 收件人列表
_To_List = ["receiver1@163.com", "receiver2@qq.com"]
Subject = "这是邮件主题"
Msg_Body = "这里是邮件的内容部分"
Attachment_Dir = "./files/attachments"


# 发送邮件
def get_message(_subject="", _body="", _from="", _to=""):
    message = MIMEMultipart()
    message['Subject'] = _subject
    message['From'] = _from
    message['To'] = _to
    message['Accept-Language'] = "zh-CN"
    message['Accept-Charset'] = "ISO-8859-1,utf-8"

    text_part = MIMEText(_text=_body, _charset="utf-8")
    message.attach(text_part)

    filelist = os.listdir(Attachment_Dir)
    if filelist is not None and len(filelist) > 0:
        for f in filelist:
            filename = Attachment_Dir + "/" + f
            file_part = MIMEText(_text=open("./files/attachments/file1.txt", "rb").read(), _charset="utf-8")
            file_part.add_header("Content-Disposition", "attachment; filename=%s" % filename.encode("utf-8"))
            message.attach(file_part)
    return message


# 发送邮件
def send_mail():
    result = {}
    succeed_receivers, failed_receivers = [], []
    result['succeed'] = {}
    result['failed'] = {}
    for receiver in _To_List:
        if re.match(r"(.+)@(.+)\.(.+)", receiver):
            try:
                sender = smtplib.SMTP(host=_Host, port=_Port)
                sender.login(_User, _Pwd)
                message = get_message(_subject=Subject, _body=Msg_Body, _from=_From, _to=receiver)
                sender.sendmail(from_addr=_From, to_addrs=receiver, msg=message.as_string())
                sender.close()
                succeed_receivers.append(receiver)
            except Exception as e:
                print("send failed to %s exception: %s" % (receiver, e.message))
                failed_receivers.append(receiver)
                continue
        else:
            print("wrong email address: %s" % (receiver,))
    succeed, failed = {}, {}
    succeed['total'], succeed['receivers'] = len(succeed_receivers), succeed_receivers
    failed['total'], failed['receivers'] = len(failed_receivers), failed_receivers
    result['succeed'], result['failed'] = succeed, failed
    return result
    pass


# 程序入口
if __name__ == '__main__':
    res = send_mail()
    for k, v in res.items():
        print("%s : %s" % (k, v))
    pass
