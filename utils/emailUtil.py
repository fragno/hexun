#!/usr/bin/env python3
#coding: utf-8

import smtplib
import getpass
from email.mime.text import MIMEText

def emailme(warning):
    sender = 'fragno12@163.com'
    receiver = 'fragno12@gmail.com'
    subject = '基金报告'
    smtpserver = 'smtp.163.com'
    username = 'fragno12'
    password = getpass.getpass("Enter Email Password: ")

    msg = MIMEText('<html><h3>' + warning + '</h3></html>','html','utf-8')
    
    msg['Subject'] = subject
    
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == "__main__":
    a = "你好dadsadasd大苏打大赛发"
    emailme(a)
