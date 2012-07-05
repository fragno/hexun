# -*- coding: utf8 -*-
#! /etc/bin/env python

import sys
sys.path.append("..")

from db.dbAPI import connect, create, insert
from utils.timeUtil import getdayofday

from utils.emailUtil import emailme

def dayDhl():
    cxn = connect("mysql", "hexunFund")
    cur = cxn.cursor()
    cur.execute("SELECT DHL FROM hx002011 ORDER BY TIME DESC LIMIT 1")
    for rowdata in cur.fetchall():
        print rowdata
        if float(rowdata[0]) < -0.0 or float(rowdata[0]) > 0.0:
            cur.execute("SELECT * FROM hx002011 ORDER BY TIME DESC LIMIT 0, 10")
            #beforeValid = False
            emailStr = "<table border='1'><th>时间</th><th>代码</th><th>基金名称</th><th>基金净值</th><th>累计净值</th><th>日涨跌</th><th>申购</th><th>赎回</th>"
            emailStr = emailStr.decode('utf8')
            #emailStr = "<table border='1'>"
            for rowdata in cur.fetchall():
                #if float(rowdata[-3]) < -1.0 or float(rowdata[-3]) > 1.0 or beforeValid == True:
                    #beforeValid = True
                emailStr += "<tr>"
                for s in rowdata:
                    emailStr += "<td><font color='#FDD0EC'>%s</font></td>" % (s,)
                    #print s
                emailStr += "</tr>"
            emailStr += "</table>"
            emailStr = emailStr.encode("utf8")
            #print emailStr
            emailme(emailStr)
    cur.close()
    cxn.close()

def main():
    dayDhl()

if __name__ == '__main__':
    main()

