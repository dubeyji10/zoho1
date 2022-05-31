from cmath import log
from datetime import date, datetime ,timedelta
from email.policy import default
import sys
import time
import logging
import mysql.connector
from mysql.connector import Error
import json
import re
from apiCall import pushInto
query = "select * FROM clients"
queryLeads = "select * FROM leads"
queryConversation = "select * FROM conversation"
queryInvoiceItems = "select * FROM invoice_items"
queryInvoiceInfo = "select * FROM invoice_info"
alpha = re.compile(r"[a-z|A-Z]|[!@#$%^&*/]")


'''logging'''
now = datetime.now()
fileName = now.strftime('%Y_%m_%d_%H_%M_%S')
logging.basicConfig(filename="outputs2/"+fileName+"_testing_3"+".log", level=logging.INFO)
logging.info("-- operations started at {} (test time = 2015 Jan 3 11:00) --".format(time.ctime()))


'''
    example : select * FROM clients WHERE added_on between '2015-01-07 10:00:00' and '2015-01-07 10:10:00'
    add quotes
'''

global insertionsClients,insertionsConversation , insertionsLeads , insertionsInvoiceItems,insertionsInvoiceInfo
insertionsClients = 0
insertionsConversation = 0
insertionsLeads = 0
insertionsInvoiceItems = 0
insertionsInvoiceInfo = 0

# aDate = datetime(2015,1,7,10,00)
# secondDate = aDate
# secondDate is the result of timedelta
'''
    second run 10:00 Jan 2 2015
'''
aDate = datetime(2015,1,2,11,00)
secondDate = aDate


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
    logging.info(' --connection successful at \'{}\' --'.format(time.ctime()))

    while True:

        if aDate > datetime(2015,1,2,18,00):
            print("done exiting now at {}".format(datetime(2015,1,2,18,00).strftime('%Y-%m-%d %H:%M:%S')))
            logging.info(' --exiting at \'{}\' timestamp : {} --'.format(time.ctime(),aDate))
            break

        print('>>infinite loop with time update<<')
        # create a cursor
        cursor = connection.cursor()
        print('waiting for 10 minutes')
        time.sleep(10) # 10 seconds now
        timestamp1 , timestamp2 = updateTime()
        timeCond = " WHERE added_on between '{}' and '{}'".format(timestamp1, timestamp2)
        logging.info('\n -- condition : {} --\n'.format(timeCond))
        # queryCondition = query + " WHERE added_on between '2015-01-08 11:20:00' and '2015-01-08 19:30:00' "
        print('-'*100)
        print('-->>records : ',timeCond,'\n')
        print("1. running for clients ")
        logging.info(' --1. running for clients at \'{}\' timestamp  : {} --'.format(time.ctime(),timestamp2))
        queryCondition = query+timeCond
        result = cursor.execute(queryCondition)
        clients_table = cursor.fetchall()
        # print(type(clients_table))
        if not clients_table:
            print(" - no records - empty list retuned")
            logging.info('\tno clients inserted')
        else:
            insertionsClients+=1
            # clients_table = cursor.fetchone()
            print("1. table fetched successfully ,insertionsClients = ",insertionsClients)
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
            fileName = 'outputs2/clients_'+str(insertionsClients)+'_temp.json'

            with open(fileName,'w',encoding='utf-8') as clientJson:
                clientJson.write(json.dumps(
                    {"data":client_collection_list},indent=4,default=str,sort_keys=True
                    ))
            
            cursor.close()
            logging.info('\t {} clients inserted'.format(len(client_collection_list)))
            logging.info('____________________________________________')
            logging.info("| caling api to push clients |")
            responseClient = pushInto('clients',json.dumps(
                    {"data":client_collection_list},indent=4,default=str,sort_keys=True
                    ))
                # print('-'*50)
            # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
            # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
            responseText = ''
            responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseClient.text)
            logging.info(responseText)
            logging.info('____________________________________________')

            print('cursor closed at ',time.ctime())
            print("done check - ",fileName)
        # ------------------------------------------------------------------------------
        print("2. running for conversation ")
        logging.info(' --2. running for conversation at \'{}\' --  timestamp  : {} '.format(time.ctime(),timestamp2))
        cursor = connection.cursor()
        queryCondition = queryConversation+timeCond
        result = cursor.execute(queryCondition)
        conversation_table = cursor.fetchall()
        # print(type(clients_table))
        if not conversation_table:
            print(" - no records - empty list retuned")
            logging.info(' \t no records created for conversation ')

        else:
            insertionsConversation+=1
            # clients_table = cursor.fetchone()
            print("1. table fetched successfully ,insertionsConversation = ",insertionsConversation)
            conversation_collection_list = []
            for rows in conversation_table:
                conversation_collection = {}
                # convert it to string otherwise it raises error
                s_n = rows[0]
                name = str(s_n)
                with_email = rows[1]
                user_id = rows[2]
                added_on = str(rows[3])
                msg = rows[5]
                conversation_collection['Name'] = name
                conversation_collection['user_id'] = user_id
                conversation_collection['with_email'] = with_email
                conversation_collection['added_on'] = added_on.replace(' ','T') + '+05:30'
                conversation_collection['msg'] = msg
                # print(json.dumps(client_collection))
                conversation_collection_list.append(conversation_collection)
            fileName = 'outputs2/conversation_'+str(insertionsConversation)+'_temp.json'
            with open(fileName,'w',encoding='utf-8') as conversationJson:
                conversationJson.write(json.dumps(
                    {"data":conversation_collection_list},indent=4,default=str,sort_keys=True
                    ))
            logging.info('\t {} conversation inserted'.format(len(conversation_collection_list)))
            logging.info('____________________________________________')
            logging.info("| caling api to push conversations |")
            responseConversation = pushInto('conversation',json.dumps(
                    {"data":conversation_collection_list},indent=4,default=str,sort_keys=True
                    ))
                # print('-'*50)
            # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
            # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
            responseText = ''
            responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseConversation.text)
            logging.info(responseText)
            logging.info('____________________________________________')

            cursor.close()
            print('cursor closed at ',time.ctime())

            print("done check - ",fileName)
        # ------------------------------------------------------------------------------
        print("3. running for leads ")
        logging.info(' --3. running for leads at \'{}\' -- timestamp  : {} '.format(time.ctime(),timestamp2))
        cursor = connection.cursor()
        queryCondition = queryLeads+timeCond
        result = cursor.execute(queryCondition)
        leads_table = cursor.fetchall()
        # print(type(clients_table))
        if not leads_table:
            print(" - no records - empty list retuned")
            logging.info(' \t no records created for leads ')

        else:
            insertionsLeads+=1
            # clients_table = cursor.fetchone()
            print("1. table fetched successfully ,insertionsLeads = ",insertionsLeads)
            leads_collection_list = []
            for rows in leads_table:
                leads_collection = {}
                # convert it to string otherwise it raises error
                local_id = rows[0]
                name = str(local_id)
                client_id = rows[1]
                lead_source = rows[2]
                importance = rows[3]
                added_on = str(rows[4])
                user_id = rows[5]
                requirement = rows[6]
                status = rows[12]
                invoice_id = rows[14]

                leads_collection['Name'] = name
                leads_collection['user_id'] = user_id
                leads_collection['client_id'] = client_id
                leads_collection['added_on'] = added_on.replace(' ','T') + '+05:30'
                leads_collection['local_id'] = local_id
                leads_collection['Last_Name'] = '(lead)'
                leads_collection['lead_source'] = lead_source
                leads_collection['source'] = lead_source
                leads_collection['requirement'] = requirement
                leads_collection['status'] = status
                leads_collection['invoice_id'] = invoice_id
                # print(json.dumps(client_collection))
                leads_collection_list.append(leads_collection)

            fileName = 'outputs2/leads_'+str(insertionsLeads)+'_temp.json'

            with open(fileName,'w',encoding='utf-8') as leadsJson:
                leadsJson.write(json.dumps(
                    {"data":leads_collection_list},indent=4,default=str,sort_keys=True
                    ))

            logging.info('\t {} leads inserted'.format(len(leads_collection_list)))
            logging.info('____________________________________________')
            logging.info("| caling api to push leads |")
            responseLeads = pushInto('Leads',json.dumps(
                    {"data":leads_collection_list},indent=4,default=str,sort_keys=True
                    ))
                # print('-'*50)
            # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
            # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
            responseText = ''
            responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseLeads.text)
            logging.info(responseText)
            logging.info('____________________________________________')
            
            cursor.close()
            print('cursor closed at ',time.ctime())
            print("done check - ",fileName)

        # -----------------------------invoice items -------------------------------------------------
        print("4. running for invoiceItems ")
        logging.info(' --4. running for invoice items at \'{}\' --  timestamp  : {} '.format(time.ctime(),timestamp2))
        cursor = connection.cursor()
        queryCondition = queryInvoiceItems+timeCond
        result = cursor.execute(queryCondition)
        invoiceItems_table = cursor.fetchall()
        # print(type(clients_table))
        if not invoiceItems_table:
            print(" - no records - empty list retuned")
            logging.info(' \t no records created for invoiceItems ')
        else:
            insertionsInvoiceItems+=1
            # clients_table = cursor.fetchone()
            print("1. table fetched successfully ,insertionsInvoiceItems = ",insertionsInvoiceItems)
            invoiceItems_collection_list = []
            for rows in invoiceItems_table:
                invoiceItems_collection = {}
                # convert it to string otherwise it raises error
                local_id = rows[0]
                name = str(local_id)
                invoice_id = rows[1]
                Query_items = rows[4]
                amount = rows[7]
                importance = rows[3]
                # added_on = str(rows[4])
                added_on = str(rows[11])
                user_id = rows[12]
                payment_status = rows[13]
                invoiceItems_collection['Name'] = name
                invoiceItems_collection['user_id'] = user_id
                invoiceItems_collection['added_on'] = added_on.replace(' ','T') + '+05:30'
                invoiceItems_collection['local_id'] = local_id
                invoiceItems_collection['payment_status'] = payment_status
                invoiceItems_collection['invoice_id'] = invoice_id
                invoiceItems_collection['query'] = Query_items
                invoiceItems_collection['Amount'] = amount
                invoiceItems_collection_list.append(invoiceItems_collection)

            fileName = 'outputs2/invoiceItems_'+str(insertionsInvoiceItems)+'_temp.json'
            cursor.close()
            with open(fileName,'w',encoding='utf-8') as invoiceItemsJson:
                invoiceItemsJson.write(json.dumps(
                    {"data":invoiceItems_collection_list},indent=4,default=str,sort_keys=True
                    ))
        
            logging.info('\t {} invoice items inserted'.format(len(invoiceItems_collection_list)))
            logging.info('____________________________________________')
            logging.info("| caling api to push invoice items |")
            responseInvoiceItems = pushInto('invoice_items',json.dumps(
                    {"data":invoiceItems_collection_list},indent=4,default=str,sort_keys=True
                    ))
                # print('-'*50)
            # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
            # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
            responseText = ''
            responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseInvoiceItems.text)
            logging.info(responseText)
            logging.info('____________________________________________')
            
            print('cursor closed at ',time.ctime())
            print("done check - ",fileName)
        # -----------------------------invoice info -------------------------------------------------
        print("5. running for invoiceInfo ")
        logging.info(' --5. running for invoice info at \'{}\' -- timestamp  : {} '.format(time.ctime(),timestamp2))
        cursor = connection.cursor()
        queryCondition = queryInvoiceInfo+timeCond
        result = cursor.execute(queryCondition)
        invoiceInfo_table = cursor.fetchall()
        # print(type(clients_table))
        if not invoiceInfo_table:
            print(" - no records - empty list retuned")
            logging.info(' \t no records created for invoice info at ')

        else:
            insertionsInvoiceInfo+=1
            # clients_table = cursor.fetchone()
            print("1. table fetched successfully ,insertionsInvoiceInfo = ",insertionsInvoiceInfo)
            invoiceInfo_collection_list = []
            for rows in invoiceInfo_table:
                invoiceInfo_collection = {}
                # convert it to string otherwise it raises error
                local_id = rows[0]
                name = str(local_id)
                invoice_no = rows[1]
                invoice_of = rows[2]
                Company_Name = rows[4]
                Customer_Name = rows[3]
                user_id = rows[13]
                added_on = str(rows[14])
                payment_detail = rows[15]
                payment_in = rows[17]
                amount_recieved = rows[19]
                sale_amount = rows[24]
                invoiceInfo_collection['Name'] = name
                invoiceInfo_collection['user_id'] = user_id
                invoiceInfo_collection['added_on'] = added_on.replace(' ','T') + '+05:30'
                invoiceInfo_collection['local_id'] = local_id
                invoiceInfo_collection['payment_detail'] = payment_detail
                invoiceInfo_collection['invoice_id'] = invoice_id
                invoiceInfo_collection['payment_in'] = payment_in
                invoiceInfo_collection['amount_recieved'] = amount_recieved
                invoiceInfo_collection['sale_amount'] = sale_amount
                invoiceInfo_collection_list.append(invoiceInfo_collection)

            fileName = 'outputs2/invoiceInfo_'+str(insertionsInvoiceInfo)+'_temp.json'
            
            cursor.close()
            with open(fileName,'w',encoding='utf-8') as invoiceInfoJson:
                invoiceInfoJson.write(json.dumps(
                    {"data":invoiceInfo_collection_list},indent=4,default=str,sort_keys=True
                    ))
        
            logging.info('\t {} invoice items inserted'.format(len(invoiceItems_collection_list)))
            logging.info('____________________________________________')
            logging.info("| caling api to push invoice info |")
            responseInvoiceInfo = pushInto('invoice_info',json.dumps(
                    {"data":invoiceInfo_collection_list},indent=4,default=str,sort_keys=True
                    ))
                # print('-'*50)
            # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
            # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
            responseText = ''
            responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseInvoiceInfo.text)
            logging.info(responseText)
            logging.info('____________________________________________')
            
      
            print('cursor closed at ',time.ctime())
            print("done check - ",fileName)

        print('-'*100)
        print("a cycle is complete")

except Error as e:
    print("error occurred",e)

finally:
    print("closed db connection")
    logging.info("closed conection")
    sys.exit()

