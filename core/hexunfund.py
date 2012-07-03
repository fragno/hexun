#! /usr/bin/env python
'''
software name:   hexun fund data analyser
author:          kris
date: 
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




for i in range(-30, 0):
    enddate = str(getdayofday(i))
    url = "http://jingzhi.funds.hexun.com/jz/kaifang.aspx?&subtype=4" + "&enddate=" + enddate
    html_src = urllib2.urlopen(url) #download html source

    ##############encode problem solve#################################################
    parser = BeautifulSoup(html_src, fromEncoding="gbk")
    ###################################################################################

    # for debug
    '''
    htmlFile = open('htmlfil.txt', 'w')
    htmlFile.write(str(parser))
    htmlFile.close()
    '''

    # for debug
    #html_src = open('htmlfil.txt', 'r')
    #parser = BeautifulSoup(html_src)

    #scroll_title = parser.findAll(attrs={'id':'scroll_title'})
    scroll_list = parser.findAll('table', attrs={'id':'scroll_list'})

    #connect to the database "hexunFund.db"
    cxn = connect("mysql", "hexunFund")
    cur = cxn.cursor()
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
        del rowData[1]
        del rowData[7]
        del rowData[10]
        del rowData[9]
        insert(cur, 'mysql', tuple(rowData))

    cur.close()
    cxn.commit()
    cxn.close()
    os.system("notify-send 'HexunFund' 'Baby Done'")
