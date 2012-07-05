#! /usr/bin/env python
'''
software name:   hexun fund data analyser
author:          kris
date:            2012.07.01
version:         1.0
'''



import os
import sys
sys.path.append("..")

import urllib, urllib2
from BeautifulSoup import BeautifulSoup
import re
from db.dbAPI import connect, create, insert

from utils.timeUtil import getdayofday
from dataProcess import dayDhl 

#
#function:    create new database from the hexun fund website
#parameters:  days: how many days of data you want to include, including today
#             flag: indicate whether create a new table
#

def NewDatabase(days, flag):
    for i in range(-1*days,0):
        enddate = str(getdayofday(i))
        url = "http://jingzhi.funds.hexun.com/jz/kaifang.aspx?&subtype=4" + "&enddate=" + enddate
        html_src = urllib2.urlopen(url) #download html source
        parser = BeautifulSoup(html_src, fromEncoding="gbk")
        scroll_list = parser.findAll('table', attrs={'id':'scroll_list'})

        #connect to the database "hexunFund.db"
        cxn = connect("mysql", "hexunFund")
        cur = cxn.cursor()
        if flag:
            create(cur)

        #print scroll_list[0].findAll('tr')[0].findAll('td')[1].contents[0].contents
        allFunds = scroll_list[0].findAll('tr')
        fundLength =  len(allFunds)
        for i in range(fundLength):
            items = allFunds[i].findAll('td')
            itemLength = len(items)
            rowData = [enddate]
            for j in range(itemLength):
                try:
                    #print items[j].contents[0].text.ljust(13,' '),
                    rowData.append(items[j].contents[0].text)
                except:
                    #print items[j].contents[0].ljust(13,' '),
                    rowData.append(items[j].contents[0])
            print rowData
            del rowData[1]
            del rowData[6]
            del rowData[9]
            del rowData[8]
            insert(cur, 'mysql', tuple(rowData))

        cur.close()
        cxn.commit()
        cxn.close()
        os.system("notify-send 'HexunFund' 'Baby Done'")


def AddTodayInfoToDb():
    enddate = str(getdayofday(-1))
    url = "http://jingzhi.funds.hexun.com/jz/kaifang.aspx?&subtype=4" + "&enddate=" + enddate
    html_src = urllib2.urlopen(url) #download html source
    parser = BeautifulSoup(html_src, fromEncoding="gbk")
    scroll_list = parser.findAll('table', attrs={'id':'scroll_list'})

    #connect to the database "hexunFund.db"
    cxn = connect("mysql", "hexunFund")
    cur = cxn.cursor()
    
    #print scroll_list[0].findAll('tr')[0].findAll('td')[1].contents[0].contents
    allFunds = scroll_list[0].findAll('tr')
    fundLength =  len(allFunds)
    for i in range(fundLength):
        items = allFunds[i].findAll('td')
        itemLength = len(items)
        rowData = [enddate]
        for j in range(itemLength):
            try:
                #print items[j].contents[0].text.ljust(13,' '),
                rowData.append(items[j].contents[0].text)
            except:
                #print items[j].contents[0].ljust(13,' '),
                rowData.append(items[j].contents[0])
        del rowData[1]
        del rowData[6]
        del rowData[9]
        del rowData[8]
        insert(cur, 'mysql', tuple(rowData))

    cur.close()
    cxn.commit()
    cxn.close()
    os.system("notify-send 'HexunFund' 'Baby Done'")

def main():
    AddTodayInfoToDb()
    #dayDhl()
    #NewDatabase(4,0)

if __name__=="__main__":
    main()


