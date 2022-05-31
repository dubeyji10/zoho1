import mysql.connector
from mysql.connector import Error

import json
from datetime import date, datetime ,timedelta
import time

# created_at between '2011-03-17 06:42:10' and '2011-03-17 07:42:50';
print("trying to connect to database")

url = "https://www.zohoapis.in/crm/v2/Leads"

line = "\n ------------------------------------ \n"
modulesList = ['Leads','clients','conversation','invoice_items','invoice_info']


# url = "https://www.zohoapis.in/crm/v2/conversation"
# url = "https://www.zohoapis.in/crm/v2/clients"
'''
    all modules queries
'''

leads_Query = ''
clients_Query = ''
conversation_Query = ''
invoiceItems_Query = ''
# invoiceInfo_Query = ''

with open('leads/leadsQuery.txt', 'r') as file:
    data = file.read()
    leads_Query += data.rstrip()
with open('clients/clientsQuery.txt', 'r') as file:
    data = file.read()
    clients_Query += data.rstrip()
with open('conversation/conversationQuery.txt', 'r') as file:
    data = file.read()
    conversation_Query += data.rstrip()
with open('invoice_items/invoice_itemsQuery.txt', 'r') as file:
    data = file.read()
    invoiceItems_Query += data.rstrip()
# with open('invoice_info/invoice_infoQuery.txt', 'r') as file:
#     data = file.read()
#     invoiceInfo_Query += data.rstrip()


aDate = datetime(2015,1,10,10,00)
shiftEndAt = datetime(2015,1,10,20,00)


def updateTime(dateTimeObject):
    # global aDate
    print("waiting for 10 minutes - all records inserted in next ten minutes to be considered")
    time.sleep(10) 
    # 10 seconds --- now ---
    # after 10 seconds later change it to 60*10 -- 10 minutes
    # or just remove it since time delta is calculate after 10 minute wait alread no need to sleep here
    # dont remove delay is not added in infinite loop for now use delay here
    '''
    
    pass the datetime object

    wait for 10 minutes 
    query all records in the last 10 minutes

    '''
    dt_string = dateTimeObject.strftime('%Y-%m-%d %H:%M:%S')
    diff = dateTimeObject + timedelta(minutes=10) 
    dateTimeObject = diff
    dt_string_diff = diff.strftime('%Y-%m-%d %H:%M:%S')

    leads_Query_withTimestamp = leads_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    clients_Query_withTimestamp = clients_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    conversation_Query_withTimestamp = conversation_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    # invoiceInfo_withTimestamp = invoiceInfo_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    invoiceItems_withTimestamp = invoiceItems_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    UpdatedQueriesList = [leads_Query_withTimestamp , clients_Query_withTimestamp ,
                conversation_Query_withTimestamp ,
                invoiceItems_withTimestamp
                ]
    return [diff , UpdatedQueriesList]


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test_export_genius_2',
                                         user='dubeyji',
                                         password='password')

    print('\n\n--connection successful--\n\n')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.close()
        # loop through all 5 table queries and create new cursor to execute them
        [aDate , queriesList] = updateTime(aDate) 
        print("now aDate var : {}".format(aDate))

        for i in queriesList:
            print("running ... ",i[-100:])
            newCursor = connection.cursor()
            result = newCursor.execute(i)
            queryOutput = newCursor.fetchall()
            outPut = queryOutput[0]
            print('-'*50)
            print("final : \n\n\n")
            print("-> output  : \n\n",outPut[0])
            print("\n\ntype -> ",type(outPut[0]),len(outPut))

        print('-'*50)

except Error as e:
    print("\n\nError while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
