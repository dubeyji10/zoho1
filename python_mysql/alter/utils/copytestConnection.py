from cmath import log
from datetime import date, datetime ,timedelta
import sys
import time
import logging
import mysql.connector
from mysql.connector import Error
import json
import re
from authentication import generateAccessTokens
from authentication import refreshTokens


# from apiCall import pushInto

global clientCounter, convCounter , leadsCounter ,invoiceInfoCounter

'''logging'''
now = datetime.now()
fileName = now.strftime('%Y_%m_%d_%H_%M_%S')
logging.basicConfig(filename="TestAuth"+'_counter_1'+".log", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logging.info("-- operations started at {} (test time = 2015 Jan 3 10:00) --".format(time.ctime()))

logging.info("-- generating access tokens at {} (test time = 2015 Jan 3 10:00) --".format(time.ctime()))
oauthResponse = generateAccessTokens()
logging.info("-- response recieved : \n {} \n\n -- at {}  --".format(oauthResponse.text,time.ctime()))



'''
    queries
'''
queryClients = "select id,company_name,phone_no,email,user_id,added_on FROM clients"
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
aDate = datetime(2015,1,3,10,00)
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

while aDate < datetime(2015,1,3,19,00):
    print('--in the loop--')
    print('waiting for 10 minutes')
    logging.info('--------------------- 10 minute wait ----------------------------\ncounter = {}'.format(counter))
    time.sleep(10) # 10 seconds now
    # time.sleep(60) # 60 seconds now
    # waiting for 1minute -------- test -------------
    timestamp1 , timestamp2 = updateTime()
    timeCond = " WHERE added_on between '{}' and '{}'".format(timestamp1, timestamp2)
    '''
        wait complete timestamps updated now check for refresh
    '''
    if counter%4==0:
        logging.info('|-----------------------------------------------------------------------|')
        print("minutes passed = ",10*counter,'(counter = ',counter,')')
        # logging.info('\n\nnow counter is set to {}\n\n'.format(0))
        logging.info(" - - - - refreshing tokens at {} - - - - - ".format(time.ctime()))
        refreshResponse = refreshTokens()
        logging.info("-- response recieved : \n {}\n\n -- at {}  --".format(refreshResponse.text,time.ctime()))
        # counter = 0
        logging.info('|-----------------------------------------------------------------------|')
    else:
        print('not running refresh token function')
        logging.info('minutes passed = {} counter = {}'.format(10*counter,counter))

    print('condition no {} : {} '.format(counter,timeCond))
    # everytime a new query is generated connect to db and perform operations
    # since keeping a connection alive is not good enough
    # not possible to keep alive the mysql connection
    with mysql.connector.connect(host='localhost',database='test_export_genius_2',user='dubeyji',password='password') as connectPointer:
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
            for rows in result:
                clientCounter+=1
                print(rows,'\n',type(rows))
        # conversations
        with connectPointer.cursor() as aCursor:
            print('2. fetching conversations')
            logging.info('2. fetching conversations')
            aCursor.execute(queryConversation+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no conversations created in the last 10 minutes <--')
            for rows in result:
                convCounter+=1
                print(rows,'\n',type(rows))
        # leads
        with connectPointer.cursor() as aCursor:
            print('3. fetching leads')
            logging.info('3. fetching leads')
            aCursor.execute(queryLeads+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no leads created in the last 10 minutes <--')
            for rows in result:
                leadsCounter+=1
                print(rows,'\n',type(rows))
        # leads
        with connectPointer.cursor() as aCursor:
            print('4. fetching invoice info')
            logging.info('4. fetching invoice info')

            aCursor.execute(queryInvoiceInfo+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no invoice info created in the last 10 minutes <--')
            for rows in result:
                invoiceInfoCounter+=1
                print(rows,'\n',type(rows))
                
        

    print('[]'*50)


print('total\n clients {} ,\n conversations {} ,\n leads {},\n invoice info {}'.format(clientCounter,convCounter,leadsCounter,invoiceInfoCounter))
logging.info("-- operations closed at {} (test time = 2015 Jan 3 10:00) --".format(time.ctime()))
logging.info('total\n clients {} ,\n conversations {} ,\n leads {},\n invoice info {}'.format(clientCounter,convCounter,leadsCounter,invoiceInfoCounter))

# mistake corrected - counter was incremented twice

