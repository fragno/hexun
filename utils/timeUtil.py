
#!/usr/bin/python 
''''' 
Filename: "utildate.py" 
author:   "zhangsong" 
date  :   "2009-03-24" 
version:  "1.00" 
''' 
from time import strftime, localtime 
from datetime import timedelta, date 
import calendar 
  
year = strftime("%Y",localtime()) 
mon  = strftime("%m",localtime()) 
day  = strftime("%d",localtime()) 
hour = strftime("%H",localtime()) 
min  = strftime("%M",localtime()) 
sec  = strftime("%S",localtime()) 
  
  
def today(): 
    ''''' 
    get today,date format="YYYY-MM-DD" 
    ''' 
    return date.today() 
  
def todaystr(): 
    ''''' 
    get date string 
    date format="YYYYMMDD" 
    ''' 
    return year+mon+day 
  
def datetime(): 
    ''''' 
    get datetime,format="YYYY-MM-DD HH:MM:SS" 
    ''' 
    return strftime("%Y-%m-%d %H:%M:%S",localtime()) 
  
def datetimestr(): 
    ''''' 
    get datetime string 
    date format="YYYYMMDDHHMMSS" 
    ''' 
    return year+mon+day+hour+min+sec 
  
def getdayofday(n=0): 
    ''''' 
    if n>=0,date is larger than today 
    if n<0,date is less than today 
    date format = "YYYY-MM-DD" 
    ''' 
    if(n<0): 
        n = abs(n) 
        return date.today()-timedelta(days=n) 
    else: 
        return date.today()+timedelta(days=n) 
  
def getdaysofmonth(year,mon): 
    ''''' 
    get days of month 
    ''' 
    return calendar.monthrange(year, mon)[1] 
  
def getfirstdayofmonth(year,mon): 
    ''''' 
    get the first day of month 
    date format = "YYYY-MM-DD" 
    ''' 
    days="01" 
    if(int(mon)<10): 
        mon = "0"+str(int(mon)) 
    arr = (year,mon,days) 
    return "-".join("%s" %i for i in arr) 
  
def getlastdayofmonth(year,mon): 
    ''''' 
    get the last day of month 
    date format = "YYYY-MM-DD" 
    ''' 
    days=calendar.monthrange(year, mon)[1] 
    mon = addzero(mon) 
    arr = (year,mon,days) 
    return "-".join("%s" %i for i in arr) 
  
def get_firstday_month(n=0): 
    ''''' 
    get the first day of month from today 
    n is how many months 
    ''' 
    (y,m,d) = getyearandmonth(n) 
    d = "01" 
    arr = (y,m,d) 
    return "-".join("%s" %i for i in arr) 
  
def get_lastday_month(n=0): 
    ''''' 
    get the last day of month from today 
    n is how many months 
    ''' 
    return "-".join("%s" %i for i in getyearandmonth(n)) 
   
def get_today_month(n=0): 
    ''''' 
    get last or next month's today 
    n is how many months 
    date format = "YYYY-MM-DD" 
    ''' 
    (y,m,d) = getyearandmonth(n) 
    arr=(y,m,d) 
    if(int(day)<int(d)): 
        arr = (y,m,day) 
    return "-".join("%s" %i for i in arr) 
  
def getyearandmonth(n=0): 
    ''''' 
    get the year,month,days from today 
    befor or after n months 
    ''' 
    thisyear = int(year) 
    thismon = int(mon) 
    totalmon = thismon+n 
    if(n>=0): 
        if(totalmon<=12): 
            days = str(getdaysofmonth(thisyear,totalmon)) 
            totalmon = addzero(totalmon) 
            return (year,totalmon,days) 
        else: 
            i = totalmon/12 
            j = totalmon%12 
            if(j==0): 
                i-=1 
                j=12 
            thisyear += i 
            days = str(getdaysofmonth(thisyear,j)) 
            j = addzero(j) 
            return (str(thisyear),str(j),days) 
    else: 
        if((totalmon>0) and (totalmon<12)): 
            days = str(getdaysofmonth(thisyear,totalmon)) 
            totalmon = addzero(totalmon) 
            return (year,totalmon,days) 
        else: 
            i = totalmon/12 
            j = totalmon%12 
            if(j==0): 
                i-=1 
                j=12 
            thisyear +=i 
            days = str(getdaysofmonth(thisyear,j)) 
            j = addzero(j) 
            return (str(thisyear),str(j),days) 
  
def addzero(n): 
    ''''' 
    add 0 before 0-9 
    return 01-09 
    ''' 
    nabs = abs(int(n)) 
    if(nabs<10): 
        return "0"+str(nabs) 
    else: 
        return nabs 
 
def main(): 
    print getdayofday(0)

if __name__ == "__main__":
    main()
