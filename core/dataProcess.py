#! /etc/bin/env python

import sys
sys.path.append("..")

from db.dbAPI import connect, create, insert
from utils.timeUtil import getdayofday

from utils.emailUtil import emailme

def main():
    cxn = connect("mysql", "hexunFund")
    cur = cxn.cursor()
    cur.execute("SELECT DHL FROM funds WHERE CODE='002011' ORDER BY TIME DESC LIMIT 4")
    for rowdata in cur.fetchall():
        if float(rowdata[0]) < -1.5 or float(rowdata[0]) > 1.5:
            cur.execute("SELECT * FROM funds WHERE CODE='002011' ORDER BY TIME DESC LIMIT 0, 30")
            beforeValid = False
            emailStr = ""
            for rowdata in cur.fetchall():
                if float(rowdata[-3]) < -1.5 or float(rowdata[-3]) > 1.5 or beforeValid == True:
                    beforeValid = True
                    for s in rowdata:
                        emailStr += "%s  |  " % (s,)
                    emailStr += "<br>"
            emailStr = emailStr.encode("utf8")
            #print emailStr
            emailme(emailStr)
    cur.close()
    cxn.close()

if __name__ == '__main__':
    main()

