from datetime import date, datetime ,timedelta
from sqlite3 import Timestamp
import sys
import time
import mysql.connector
from mysql.connector import Error
import json

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

# ------------------------------------------------------------------ 

'''
    queries
'''
leads_Query = ''
clients_Query = ''
conversation_Query = ''
invoiceItems_Query = ''
invoiceInfo_Query = ''

with open('leads/leadsQuery.txt', 'r') as file:
    data = file.read()
    leads_Query = data.rstrip()
with open('clients/clientsQuery.txt', 'r') as file:
    data = file.read()
    clients_Query = data.rstrip()
with open('conversation/conversationQuery.txt', 'r') as file:
    data = file.read()
    conversation_Query = data.rstrip()
with open('invoice_items/invoice_itemsQuery.txt', 'r') as file:
    data = file.read()
    invoiceItems_Query = data.rstrip()
with open('invoice_info/invoice_infoQuery.txt', 'r') as file:
    data = file.read()
    invoiceInfo_Query = data.rstrip()




# ------------------------------------------------------------------ 
    # ''' execute queies and disconnect db after each query execution this should work '''
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test_export_genius_2',
                                         user='dubeyji',
                                         password='password')
    print("connected to db")
    while True:
        if aDate.strftime('%Y-%m-%d %H:%M:%S') == "2015-01-07"+" 18:00:00":
            print("shift ended thank you")
            sys.exit()
                # break
        print("infite loop started")
        print("waiting for 10 seconds")
        # after 10 minutes
        time.sleep(10)
        timestamp1,timestamp2 = updateTime()
        timeCondition = " WHERE added_on between '{}' and '{}' ".format(timestamp1.strftime('%Y-%m-%d %H:%M:%S'),timestamp2.strftime('%Y-%m-%d %H:%M:%S'))
        # print(" WHERE added_on between {} and {} ".format(timestamp1 , timestamp2))
        print("->condition  : ",timeCondition)
        # do all tables one by one looping creates error
        #  mysql db cant handle large requst
        print('-'*100)
        leads_Query_timed = leads_Query + timeCondition
        print('\n 1. leads : ',leads_Query_timed[-95:])
        print('*'*50)
        print("\n\n1. doing leads writing json for every successfull result with \n query = ",leads_Query_timed)
        cursor = connection.cursor()
        result = cursor.execute(leads_Query_timed)
        leadsOutput = cursor.fetchall()
        outPut = leadsOutput[0]
        if outPut==None:
            print("\n\nno output for leads between {} and {} ".format(timestamp1 , timestamp2))
        else:
            fileName = 'outputs/leads_BETWEEN_' +timestamp1.strftime('%Y_%m_%d_%H_%M_%S')+"and"+timestamp2.strftime('%Y_%m_%d_%H_%M_%S')+"_result.json"
            with open(fileName,'w',encoding='utf8') as outFile:
                outFile.write(outPut[0])
            print("check file : ",fileName)
            cursor.close()
            # connection.close()
        print('*'*50)

        # clients_Query_timed = clients_Query + timeCondition
        # print('\n 2. clients : ',clients_Query_timed[-95:])
        # conversation_Query_timed = conversation_Query + timeCondition
        # print('\n 3. conversation : ',conversation_Query_timed[-95:])
        # invoiceInfo_Query_timed = invoiceInfo_Query + timeCondition
        # print('\n 4. invoice info : ',invoiceInfo_Query_timed[-95:])
        # invoiceItems_Query_timed = invoiceItems_Query + timeCondition
        # print('\n 5. invoice items : ',invoiceItems_Query_timed[-95:])
        # print('-'*100)

        # print('\n\n--connection successful--\n\n')
        # # create a cursor to query
        # print('/\\'*25)
    
except Error as e:
    print("\n\nError while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        
    print("MySQL connection is closed")
    sys.exit()

