from datetime import date, datetime ,timedelta
import sys
import time
import mysql.connector
from mysql.connector import Error
import json
import re

query = "select * FROM clients"
queryLeads = "select * FROM leads"
queryConversation = "select * FROM conversation"

'''
    example : select * FROM clients WHERE added_on between '2015-01-07 10:00:00' and '2015-01-07 10:10:00'
    add quotes
'''
global insertionsClients,insertionsConversation
insertionsClients = 0
insertionsConversation = 0

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

    while True:

        if aDate.strftime('%Y-%m-%d %H:%M:%S') == "2015-01-07 18:00:00":
            print("done exiting now")
            sys.exit()

        print('>>infinite loop with time update<<')
        # create a cursor
        cursor = connection.cursor()
        print('waiting for 10 minutes')
        time.sleep(10) # 10 seconds now
        timestamp1 , timestamp2 = updateTime()
        timeCond = " WHERE added_on between '{}' and '{}'".format(timestamp1, timestamp2)
        # queryCondition = query + " WHERE added_on between '2015-01-08 11:20:00' and '2015-01-08 19:30:00' "
        print('-'*100)
        print('-->>records : ',timeCond,'\n')
        print("1. running for clients ")
        queryCondition = query+timeCond
        result = cursor.execute(queryCondition)
        clients_table = cursor.fetchall()
        # print(type(clients_table))
        if not clients_table:
            print(" - no records - empty list retuned")
        else:
            insertionsClients+=1
            # clients_table = cursor.fetchone()
            print("1. table fetched successfully ,insertionsClients = ",insertionsClients)
            alpha = re.compile(r"[a-z|A-Z]|[!@#$%^&*/]")
            client_collection_list = []
            for rows in clients_table:
                client_collection = {}
                # convert it to string otherwise it raises error
                phoneNo = str(rows[5])
                local_id = rows[0]
                name = rows[3]
                company_grade = rows[4]
                address = rows[10]
                user_id = rows[12]
                added_on = str(rows[13])
                last_conv = rows[14]
                if not bool(re.search(alpha,phoneNo)):
                    client_collection['phone_no'] = phoneNo
                    # print("{ 'phone_no' : ",phoneNo,"}")
                else:
                    client_collection['phone_no'] = None
                    # print("{ 'phone_no' : ","'null'","}")
                client_collection['Name'] = name
                client_collection['user_id'] = user_id
                client_collection['local_id'] = local_id
                client_collection['added_on'] = added_on.replace(' ','T') + '+05:30'
                client_collection['last_conversation'] = last_conv
                # print(json.dumps(client_collection))
                client_collection_list.append(client_collection)
            fileName = 'outputs/clients_'+str(insertionsClients)+'_temp.json'
            with open(fileName,'w',encoding='utf-8') as clientJson:
                json.dump({"data":client_collection_list},clientJson,sort_keys=True)
            cursor.close()
            print('cursor closed at ',time.ctime())
            print("done check - ",fileName)
        # ------------------------------------------------------------------------------
        print("2. running for conversation ")
        cursor = connection.cursor()
        queryCondition = queryConversation+timeCond
        result = cursor.execute(queryCondition)
        conversation_table = cursor.fetchall()
        # print(type(clients_table))
        if not conversation_table:
            print(" - no records - empty list retuned")
        else:
            insertionsConversation+=1
            # clients_table = cursor.fetchone()
            print("1. table fetched successfully ,insertionsConversation = ",insertionsConversation)
            alpha = re.compile(r"[a-z|A-Z]|[!@#$%^&*/]")
            conversation_collection_list = []
            for rows in conversation_table:
                conversation_collection = {}
                # convert it to string otherwise it raises error
                s_n = rows[0]
                with_email = rows[1]
                user_id = rows[2]
                added_on = str(rows[3])
                msg = rows[5]
                if not bool(re.search(alpha,phoneNo)):
                    conversation_collection['phone_no'] = phoneNo
                    # print("{ 'phone_no' : ",phoneNo,"}")
                else:
                    conversation_collection['phone_no'] = None
                    # print("{ 'phone_no' : ","'null'","}")
                conversation_collection['Name'] = name
                conversation_collection['user_id'] = user_id
                conversation_collection['with_email'] = with_email
                conversation_collection['added_on'] = added_on.replace(' ','T') + '+05:30'
                conversation_collection['msg'] = msg
                # print(json.dumps(client_collection))
                conversation_collection_list.append(conversation_collection)
            fileName = 'outputs/conversation_'+str(insertionsConversation)+'_temp.json'
            with open(fileName,'w',encoding='utf-8') as conversationJson:
                json.dump({"data":conversation_collection_list},conversationJson,sort_keys=True)
            cursor.close()
            print('cursor closed at ',time.ctime())
            print("done check - ",fileName)
        print('-'*100)
        print("a cycle is complete")

except Error as e:
    print("error occurred",e)

finally:
    print("closed db connection")