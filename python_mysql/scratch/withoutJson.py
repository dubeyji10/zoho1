from datetime import date, datetime ,timedelta
from pydoc import cli
from sqlite3 import Timestamp
import sys
import time
import mysql.connector
from mysql.connector import Error
import json
import re


global insertCount
insertCount = 0
aDate = datetime(2015,1,7,10,00)
secondDate = aDate
# secondDate is the result of timedelta

def updateTime():
    global aDate , secondDate
    d1 = aDate.strftime('%Y-%m-%d %H:%M:%S')
    d2 = secondDate.strftime('%Y-%m-%d %H:%M:%S')
    # print("before update aDate = {} , secondDate = {}".format(d1,d2))
    diff = secondDate + timedelta(minutes=10) 
    aDate = secondDate
    secondDate = diff
    # print("now after update : aDate = {} , secondDate = {}".format( aDate.strftime('%Y-%m-%d %H:%M:%S') , secondDate.strftime('%Y-%m-%d %H:%M:%S')))
    return aDate , secondDate


try:
    connection = mysql.connector.connect(host='localhost',
                                        database='test_export_genius_2',
                                        user='dubeyji',
                                        password='password')

    # create a cursor
    cursor = connection.cursor()
    query = "select * FROM clients"
    # queryCondition = query + " WHERE added_on between '2015-01-08 11:20:00' and '2015-01-08 19:30:00' "
    queryCondition = query
    result = cursor.execute(queryCondition)

    clients_table = cursor.fetchall()
    # clients_table = cursor.fetchone()
    print("1. table fetched successfully ")
    print("2. output : \n\n")
    print(clients_table)
    print("\n\ntype -> ",type(clients_table),' length : ',len(clients_table))
    print('.'*50)
    print("cursor.description : \n",cursor.description)
    desc = cursor.description
    length_ClientHeaders = len(desc)
    for (i, item) in enumerate(desc, start=0):
        print(i, item[0])

    alpha = re.compile(r"\d")

    for rows in clients_table:
        # convert it to string otherwise it raises error
        phoneNo = str(rows[5])
        
        if bool(re.search(alpha,phoneNo)):
            print(" ----- is a phone number consists only of digits ")
            print("{ 'phone_no' : ",phoneNo,"'}")
        else:
            print("{ 'phone_no' : ",'null',"}")
except Error as e:
    print("error occurred",e)

finally:
    print("closed db connection")