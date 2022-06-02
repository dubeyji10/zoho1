from datetime import date, datetime ,timedelta
import sys
import time
import logging
from requests import request
import mysql.connector
from mysql.connector import Error
import json
import re
from authentication import generateAccessTokens
from authentication import refreshTokens

from apiCall import pushInto
#
# pushInto(moduleName , payload):
# from apiCall import pushInto
#
global clientCounter, convCounter , leadsCounter ,invoiceInfoCounter

'''logging'''
now = datetime.now()
fileName = now.strftime('%Y_%m_%d_%H_%M_%S')
logging.basicConfig(filename="Version_4"+fileName+"_LOGS.log", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
#aDate = datetime(2013,7,26,10,00)
logging.info("-- operations started at {} (test time = 2014 09 23  10:00) --".format(time.ctime()))

logging.info("-- not calling generateAccessToken because already called  (test time = 2014 09 23  10:00) --")
#oauthResponse = generateAccessTokens()
#logging.info("-- response recieved : \n {} \n\n -- at {}  --".format(oauthResponse.text,time.ctime()))



'''
    queries
'''
queryClients = "select id,company_name,company_grade,phone_no,email,user_id,added_on FROM clients"
queryConversation = "select s_n,with_email,user_id,added_on,msg FROM conversation"
queryLeads = "select id,client_id,lead_source,importance,added_on,user_id,requirement,status,invoice_id FROM leads"
queryInvoiceInfo = "select Id,invoice_no,invoice_of,user_id,added_on,Email,payment_in,sale_rule,sale_amount FROM invoice_info"
# info has Id not id but it is item[index=0]
# queryInvoiceItems = "select * FROM invoice_items"
alpha = re.compile(r"[a-z|A-Z]|[!@#$%^&*/]")
counter = 0
# after every 30 minutes i.e. counter%3==0 run refreshToken.py to refresh the accessToken
clientCounter = 0
convCounter = 0
leadsCounter = 0
invoiceInfoCounter = 0

''' date variables '''

# aDate = datetime(2015,1,3,11,00)
#aDate = datetime(2015,1,3,10,00)
#aDate = datetime(2013,7,26,10,00)
#"2014-09-23"
aDate = datetime(2014,9,23,10,00)
#
# 2013-07-26
#
secondDate = aDate

# 480 minutes - till 19:00 so loop breaks at counter = 49

def updateTime():
    global aDate , secondDate , counter
    counter+=1
    # d1 = aDate.strftime('%Y-%m-%d %H:%M:%S')
    # d2 = secondDate.strftime('%Y-%m-%d %H:%M:%S')
    # print("before update aDate = {} , secondDate = {}".format(d1,d2))
    diff = secondDate + timedelta(minutes=10) 
    aDate = secondDate
    secondDate = diff
    # print("now after update : aDate = {} , secondDate = {}".format( aDate.strftime('%Y-%m-%d %H:%M:%S') , secondDate.strftime('%Y-%m-%d %H:%M:%S')))
    return aDate , secondDate

''' refresh token every 40 minutes '''

while aDate < datetime(2014,9,23,20,00):
    # counter is incremented in updateTime function
    print('--in the loop--')
    print('waiting for 10 minutes')
    logging.info('--------------------- 10 minute wait ----------------------------')
    time.sleep(2) # 2 seconds now
    # time.sleep(60) # 60 seconds now
    # waiting for 1minute -------- test -------------
    timestamp1 , timestamp2 = updateTime()
    timeCond = " WHERE added_on between '{}' and '{}'".format(timestamp1, timestamp2)
    '''
        wait complete timestamps updated now check for refresh
    '''
    if counter%4==0:
        print("minutes passed = ",10*counter,'(counter = ',counter,')')
        logging.info('minutes passed = {} , counter = {} '.format(10*counter , counter))
        
        logging.info(" - - - - refreshing tokens at {} - - - - - ".format(time.ctime()))
        refreshResponse = refreshTokens()
        logging.info("-- response recieved : \n {}\n\n -- at {}  --".format(refreshResponse.text,time.ctime()))

    print('condition no {} : {} '.format(counter,timeCond))
    # everytime a new query is generated connect to db and perform operations
    # since keeping a connection alive is not good enough
    # not possible to keep alive the mysql connection
    with mysql.connector.connect(host='localhost',database='export_genius_db',user='root',password='mainhoonna') as connectPointer:
        print('-> connection established at timestamp = {}',timestamp2)
        logging.info(' --connection established at \'{}\' timestamp  : {} --'.format(time.ctime(),timestamp2))
        # clients
        with connectPointer.cursor() as aCursor:
            print('1. fetching clients')
            logging.info('1. fetching clients')
            aCursor.execute(queryClients+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no clients created in the last 10 minutes <--')
                logging.info('__________  no clients created in the last 10 minutes  __________')

            else:
                clientCounter+=1
                # create clients payload ------------------  id,company_name,company_grade,phone_no,email,user_id,added_on
                client_collection_list = []
                for rows in result:
                    client_collection = {}
                    # convert it to string otherwise it raises error
                    local_id = rows[0]
                    name = rows[1]
                    company_grade = rows[2]
                    phoneNo = str(rows[3])
                    email = rows[4]
                    user_id = rows[5]
                    added_on = str(rows[-1])
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
                    client_collection['company_grade'] = company_grade
                    # print(json.dumps(client_collection))
                    client_collection_list.append(client_collection)
                fileName = 'outputs2/clients_'+str(clientCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":client_collection_list},indent=4,default=str,sort_keys=True
                        ))
                
                logging.info("\n\n{} clients crated \n\n".format(len(client_collection_list)))
                responseClient = pushInto('clients',json.dumps(
                    {"data":client_collection_list},indent=4,default=str,sort_keys=True
                    ))
                print('response to  clients api call : \n\n ',responseClient.text)
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseClient.text)
                logging.info(responseText)
                logging.info('____________________________________________')


                # -----------------------------------------
        # conversations
        with connectPointer.cursor() as aCursor:
            print('2. fetching conversations')
            logging.info('2. fetching conversations')
            aCursor.execute(queryConversation+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no conversations created in the last 10 minutes <--')
                logging.info('__________  no conversations created in the last 10 minutes  __________')

            else:
                convCounter+=1
                conv_Collection_List = []
                # create payloads for conversations -------------------- s_n,with_email,user_id,added_on,msg
                for rows in result:
                    convCollection = {}
                    name = str(rows[0])
                    s_n = rows[0]
                    with_email = rows[1]
                    user_id = rows[2]
                    added_on = str(rows[3])
                    msg = rows[4]
                    convCollection['Name'] = name
                    convCollection['added_on'] = added_on.replace(' ','T') + '+05:30'
                    convCollection['s_n'] = s_n
                    convCollection['msg'] = msg
                    convCollection['user_id'] = user_id
                    convCollection['with_email'] = with_email

                    conv_Collection_List.append(convCollection)
                fileName = 'outputs2/conversation'+str(convCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":conv_Collection_List},indent=4,default=str,sort_keys=True
                        ))

                logging.info('____________________________________________')
                logging.info("| caling api to push conversations |")
                responseConversation = pushInto('conversation',json.dumps(
                        {"data":conv_Collection_List},indent=4,default=str,sort_keys=True
                        ))
                    # print('-'*50)
                # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
                # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseConversation.text)
                logging.info(responseText)
                logging.info('____________________________________________')
                

                logging.info("\n\n{} conversations inserted \n\n".format(len(conv_Collection_List)))
                print('inserted conversations in ',fileName)
            



                #  -----------------------------------------------------

        # leads
        with connectPointer.cursor() as aCursor:
            print('3. fetching leads')
            logging.info('3. fetching leads')
            aCursor.execute(queryLeads+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no leads created in the last 10 minutes <--')
                logging.info('__________  no leads created in the last 10 minutes  __________')

            else:
                leadsCounter+=1
                # payloads for leads ---------------------------------
                # id,client_id,lead_source,importance,added_on,user_id,requirement,status,invoice_id
                leadsCollList = []
                for rows in result:
                    leadsColl = {}
                    local_id = rows[0]
                    name = str(local_id)
                    client_id = rows[1]
                    lead_source = rows[2]
                    importance = rows[3]
                    added_on = str(rows[4])
                    user_id = rows[5]
                    requirement = rows[5]
                    status = rows[6]
                    invoice_id = rows[7]
                    leadsColl['Name'] = name
                    leadsColl['local_id'] = local_id
                    leadsColl['client_id'] = client_id
                    leadsColl['lead_source'] = lead_source
                    leadsColl['importance'] = importance
                    leadsColl['added_on'] = added_on.replace(' ','T') + '+05:30'
                    leadsColl['requirement'] = requirement
                    leadsColl['status'] = status
                    leadsColl['invoice_id'] = invoice_id
                    leadsColl['Last_Name'] = "(lead)"

                    leadsCollList.append(leadsColl)
                print("{} leads created".format(len(leadsCollList)))


                fileName = 'outputs2/leads'+str(leadsCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
            
                logging.info('____________________________________________')
                logging.info("| caling api to push leads |")
                responseLeads = pushInto('Leads',json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
                # print('-'*50)
                # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
                # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseLeads.text)
                logging.info(responseText)
                logging.info('____________________________________________')
            
                
                logging.info("\n\n{} leads inserted \n\n".format(len(leadsCollList)))
                print('inserted leads in ',fileName)

        # invoice info
        with connectPointer.cursor() as aCursor:
            print('4. fetching invoice info')
            logging.info('4. fetching invoice info')

            aCursor.execute(queryInvoiceInfo+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no invoice info created in the last 10 minutes <--')
                logging.info('__________  no invoice info created in the last 10 minutes  __________')
            else:
                invoiceInfoCounter+=1
                # payloads for invoice info ---------------------------------
                # Id,invoice_no,invoice_of,user_id,added_on,Email,payment_in,sale_rule,sale_amount 
                invoiceInfoCollList = []
                for rows in result:
                    invInfoColl = {}
                    invInfoColl['Name'] = str(rows[0])
                    invInfoColl['invoice_no'] = rows[1]
                    invInfoColl['invoice_of'] = rows[2]
                    invInfoColl['user_id'] = rows[3]
                    added_on = str(rows[4])
                    invInfoColl['added_on'] = added_on.replace(' ','T') + '+05:30'
                    invInfoColl['Email'] = rows[5]
                    invInfoColl['payment_in'] = rows[6]
                    invInfoColl['sale_rule'] = rows[7]
                    invInfoColl['sale_amount'] = rows[8]

                    invoiceInfoCollList.append(invInfoColl)
                print("{} invoice info created".format(len(invoiceInfoCollList)))
                # ----------------------------------------------------------------  

                fileName = 'outputs2/invoiceInfo'+str(invoiceInfoCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":invoiceInfoCollList},indent=4,default=str,sort_keys=True
                        ))

                logging.info('____________________________________________')
                logging.info("| caling api to push invoice info |")
                responseInvoiceInfo = pushInto('invoice_info',json.dumps(
                        {"data":invoiceInfoCollList},indent=4,default=str,sort_keys=True
                        ))
                    # print('-'*50)
                # logging.info("\n\n\n>>>calling generic module api {}\n\n\n".format(time.ctime()))
                # responseReturned = pushIntoModule(module_name=modulesList[index],payload=leadsJson)
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),responseInvoiceInfo.text)
                logging.info(responseText)
                logging.info('____________________________________________')

                
                logging.info("\n\n{} invoice info inserted \n\n".format(len(leadsCollList)))
                print('inserted invoice info in ',fileName)

        
    print('[]'*50)


print('total\n clients {} ,\n conversations {} ,\n leads {},\n invoice info {}'.format(clientCounter,convCounter,leadsCounter,invoiceInfoCounter))
logging.info("-- operations closed at {} (test time = 2015 Jan 3 10:00) --".format(time.ctime()))
logging.info('\ntotal:\n clients {} ,\n conversations {} ,\n leads {},\n invoice info {}'.format(clientCounter,convCounter,leadsCounter,invoiceInfoCounter))


