#-*- coding: utf-8 -*-
#! /usr/bin/env python

import os
from random import randrange as rrange

COLSIZE = 10
RDBMSs = {'s':'sqlite', 'm':'mysql', 'g':'gadfly'}
DB_EXC = None

def setup():
    return RDBMSs[raw_input('''
Choose a database system:

(M)ySQL
(G)adfly
(S)QLite

Enter choice: ''').strip().lower()[0]]

def connect(db, dbName):
    global DB_EXC
    dbDir = '%s_%s' % (db, dbName)
    if db == 'sqlite':
        try:
            import sqlite3
        except ImportError, e:
            try:
                from pysqlite2 import dbapi2 as sqlite3
            except ImportError, e:
                return None

        DB_EXC = sqlite3
        if not os.path.isdir(dbDir):
            os.mkdir(dbDir)
        cxn = sqlite.connect(os.path.join(dbDir, dbName))

    elif db == 'mysql':
        try:
            import MySQLdb
            import _mysql_exceptions as DB_EXC
        except ImportError, e:
            return None

        try:
            cxn = MySQLdb.connect(db=dbName, charset='utf8')
        except DB_EXC.OperationalError, e:
            cxn = MySQLdb.connect(user='root', passwd='1009257221', charset='utf8')
            try:
                cxn.query('DROP DATABASE %s' % dbName)
            except DB_EXC.OperationalError, e:
                pass
            cxn.query("CREATE DATABASE %s" % dbName)
            cxn.query("GRANT ALL ON %s.* to ''@'localhost'" % dbName)
            cxn.commit()
            cxn.close()
            cxn = MySQLdb.connect(db=dbName, charset='utf8')

    elif db == 'gadfly':
        try:
            from gadfly import gadfly
            DB_EXC = gadfly
        except ImportError, e:
            return None

        try:
            cxn = gadfly(dbName, dbDir)
        except IOError, e:
            cxn = gadfly()
            if not os.path.isdir(dbDir):
                os.mkdir(dbDir)
                cxn.startup(dbName, dbDir)
            else:
                return None
    return cxn

def create(cur):
    try:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS funds (
        TIME VARCHAR(10),
        CODE VARCHAR(6),
        ABBR VARCHAR(50),
        UVAL NUMERIC(6,4),
        CVAL NUMERIC(5,3),
        DHL VARCHAR(20),
        SUBSCRIBE VARCHAR(10),
        REDEEM VARCHAR(10))
        ''')
       
    except DB_EXC.OperationalError, e:
        drop(cur)
        create(cur)

drop = lambda cur: cur.execute('DROP TABLE funds')

NAMES = (
('aaron', 8312), ('angela', 7603), ('dave', 7306),
('大赛davina',7902), ('elliot', 7911), ('ernie', 7410),
('jess', 7912), ('jim大赛的', 7512), ('larry', 7311),
('lesl的撒旦ie', 7808), ('melissa', 8602), ('pat', 7711),
('serena', 7003), ('stan', 7607), ('faye', 6812),
('amy', 7209),
)

def randName():
    pick = list(NAMES)
    while len(pick) > 0:
        yield pick.pop(rrange(len(pick)))

def insert(cur, db, rowData):
    if db == 'sqlite':
        cur.executemany("INSERT INTO funds VALUES(%s, %s, %s)",
                [(who, uid, rrange(1,5)) for who, uid in randName()])

    elif db == 'gadfly':
        for who, uid in randName():
            cur.execute("INSERT INTO funds VALUES(%s, %s, %s)", 
                    (who, uid, rrange(1, 5)))

    elif db == 'mysql':
       #rowData = (u'879', u'700002', u'\u5e73\u5b89\u5927\u534e\u6df1\u8bc1300', u'0.9580', u'1.0380', u'-2.45%', u'\u5f00\u653e', u'\u5f00\u653e')
       #rowData = ('1','2','2','5','6','7','8','9')
       cur.execute("INSERT INTO funds VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", rowData)
       #print rowData
                #[(who, uid, rrange(1, 5)) for who, uid in randName()])

getRC = lambda cur: cur.rowcount if hasattr(cur, 'rowcount') else -1

def update(cur):
    fr = rrange(1, 5)
    to = rrange(1, 5)
    cur.execute("UPDATE users SET prid=%d WHERE prid=%d" % (to, fr))
    return fr, to, getRC(cur)

def delete(cur):
    rm = rrange(1, 5)
    cur.execute("DELETE FROM users WHERE prid=%d" % rm)
    return rm, getRC(cur)

def dbDump(cur):
    cur.execute('SELECT * FROM users')
    print '\n%s%s%s' % ('LOGIN'.ljust(COLSIZE),
            'USERID'.ljust(COLSIZE), 'PROJ#'.ljust(COLSIZE))
    for data in cur.fetchall():
        print '%s%s%s' % tuple([str(s).title().ljust(COLSIZE) for s in data])


def main():

    db = setup()
    print '*** Connecting to %s database' % db   
    
    cxn = connect(db, 'hexunFund')
    if not cxn:
        print 'ERROR: %s not supported, exiting' % db
        return 
    cur = cxn.cursor()
        
    print '\n*** Creating users table'
    create(cur)
    cur.close()
    cxn.commit()
    cxn.close()

'''
    print '\n*** Inserting names into table'
    insert(cur, db)
    dbDump(cur)

    print '\n*** Randomly moving folks',
    fr, to, num = update(cur)
    print 'from one group (%d) to another (%d)' % (fr, to)
    print '\t(%d users moved)' % num
    dbDump(cur)

    print '\n*** Randomly choosing group',
    rm, num = delete(cur)
    print '(%d) to delete' % rm
    print '\t (%d users removed)' % num
    dbDump(cur)


    print '\n*** Dropping users table'
    #drop(cur)
'''
if __name__ == '__main__':
    main()
