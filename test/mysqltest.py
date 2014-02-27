#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="123123", db="kscudb")
cursor = db.cursor()

cursor.execute("select softwareId from softwareInfo where cid=1")
result = cursor.fetchall()

# output = open('/home/shine/other', 'w')
for record in result:
    print record[0]
    # output.write(record[0])
    # output.write("\n")
# output.close()