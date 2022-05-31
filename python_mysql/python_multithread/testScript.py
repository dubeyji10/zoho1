from cmath import log
from urllib import response
import mysql.connector
from mysql.connector import Error
from datetime import date, datetime ,timedelta
import time
import logging
import json
import requests
import sys
import threading
import shutil

'''
    scope  : 

    ZohoCRM.modules.ALL,ZohoCRM.org.ALL,ZohoCRM.modules.custom.all,ZohoCRM.users.all,ZohoCRM.org.all,ZohoCRM.settings.all

'''

'''globals'''
global leads_Query
global aDate
global payload_oauth
global totalCalls
global leadsDataToPush
global myRefreshToken
totalCalls = 0

url = "https://www.zohoapis.in/crm/v2/"


# exampleDate = '2015-01-07'
exampleDate = '2015-01-02'


'''logging'''
now = datetime.now()
fileName = now.strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename="logs/"+fileName+"_testing_3"+".log", level=logging.INFO)
logging.info("-- operations started at {} (test time = 2015 Jan 2 11:00) --".format(time.ctime()))

with open('leads/leadsQuery.txt', 'r') as file:
    data = file.read()
    leads_Query = data.rstrip()

'''
    for example sake using records from 2015 Jan 7 10:00
    2nd - for example sake using records from 2015 Jan 2 11:00
'''
# aDate = datetime(2015,1,7,10,00)
aDate = datetime(2015,1,2,11,00)
# print("running for leads - query : \n",leads_Query)
leads_Query_withTimestamp = ''

def printTimeInterval2(dateTimeObject):
    global leads_Query_withTimestamp
    print("waiting for 10 minutes")
    time.sleep(10) #10 seconds --- now ---
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
    return diff

def pushIntoLeads(payload):
    logging.info("calling leads api at {}".format(time.ctime()))
    '''
        add try except here later
    '''
    print(">make request")
    print(">write request response to log")
    print("reading accessToken.json")
    with open(accessTokenFile,'r') as client:
        tokens = json.load(client)

    accessToken = tokens['access_token']
    url_leads = url+"Leads"
    headers = {
    'Authorization': 'Bearer '+accessToken,
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", url_leads, headers=headers, data=json.dumps(payload))
    # print(response.text)
    logging.info("\n ------------------------------------ \n")
    logging.info("\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),response.text))
    logging.info("\n ------------------------------------ \n")
    print("done")

# -----------------------------------------------------------------------------------
# OAuth and Refresh Tokens
# -----------------------------------------------------------------------------------

clientFile = 'self_client.json'
with open(clientFile,'r') as client:
        payload_oauth = json.load(client)

# payload_oauth = {

#     "client_id" : "your-client-id",
#     "client_secret" : "your-client-secret" ,  
#     "grant_type": "authorization_code",
#     "code": "your-code-from-api-console",
#     "grant_type": "authorization_code"

# } 

# first part oauth
def generateAuthFunction(payload_dict):
    print('______________________________________')
    print("1. making api request using payload : \n",payload_dict)
    print("2. generating oauth token")
    print("3. got response")
    print("4. writing response to oauthResponse.json")            
    logging.info(" oauth generation at {} ".format(time.ctime()))
    # read client json

    #making the request
    files=[]
    headers = {}
    urlOAuth = "https://accounts.zoho.in/oauth/v2/token"
    response = requests.request("POST", urlOAuth, headers=headers, data=payload_dict, files=files)

    # writing reponse to oauthResponse.json
    print("\t-> response generated: \n")
    print(response.text)
    with open('oauthResponse.json','w',encoding='utf8') as oauthResponse:
        oauthResponse.write(response.text)
    print('______________________________________')
    logging.info("\n --------------------------------------------------- \n")
    logging.info("\n --- response to oauth request at {} --- \n {}".format(time.ctime,response.text))
    logging.info("\n --------------------------------------------------- \n")
    
    # return
    


def refreshToken():
    if aDate.strftime('%Y-%m-%d %H:%M:%S')>exampleDate+" 19:00:00":
        logging.info("-- done for today -- ")
        logging.info("-- stopped generating refresh tokens at {}--".format(time.ctime()))
        # for example -- stopped generating refresh tokens at 2015-01-07 18:00:00
        print("shift ended thank you closing the db connection ,kill the script")
        sys.exit()

    global totalCalls
    urlRefresh = "https://accounts.zoho.in/oauth/v2/token?"

    global accessTokenFile
    payload = None
    print("->refreshing the access tokens")
    logging.info(" -> refreshing tokens at {} ".format(time.ctime()))

    with open('self_client.json','r') as client:
        payload = json.load(client)
    print("1. creating payload for refresh request")
    myClientID = payload['client_id']
    myClientSecret = payload['client_secret']

    # read oauthResponse.json for refresh and access token 
    print("\t 1.1 read the written oauthResponse.json for access token and refresh token")
    with open('oauthResponse.json','r') as client:
        refreshTokenVar = json.load(client)
    myRefreshToken = refreshTokenVar['refresh_token']

    # print("client id : {} \n client secret : {} \n refresh token : {}".format(myClientID,
    # myClientSecret,myRefreshToken))
    print("2. thread starts ")
    # at every 120 seconds thread runs
    timer = threading.Timer(120, refreshToken) # # Call `refreshToken` in 120 seconds.
    timer.start()
    print("3. make api calls \n make changes in access_token.json")
    files=[]
    headers = {}
    logging.info(" writing refresh token request response at {} ".format(time.ctime()))

    payloadRefresh={
    'client_id': myClientID,
    'client_secret': myClientSecret,
    'refresh_token': myRefreshToken,
    'grant_type': 'refresh_token'
    }

    refreshResponse = requests.request("POST", urlRefresh, headers=headers, data=payloadRefresh, files=files)
    print("\t 3.1 response to refresh token request : \n")
    print("response : ---- \n\n",refreshResponse,'\n\n')
    # pprint.pprint(refreshResponse.text)
    print("4. writing response to accessToken.json ")
    logging.info("\n --------------------------------------------------- \n")
    logging.info("\n --- response to refresh request at {} --- \n {}".format(time.ctime(),refreshResponse.text))
    logging.info("\n --------------------------------------------------- \n")

    with open(accessTokenFile,'w') as refresh:
        refresh.write(refreshResponse.text)
    print("-done-")
    totalCalls+=1
    print('\n\n\n\n|-- total refresh access token calls {} --|\n\n\n\n'.format(totalCalls))
    print('\\/'*25)


# call generateoauth
generateAuthFunction(payload_oauth)
src="oauthResponse.json"
dst="accessToken.json"
accessTokenFile = dst
print("-> now src = {} exists and can copy as dst = {}".format(src , dst))
# write refresh token response  - access token in the accessToken.json
# shutil.copy(src,dst)
print("->created copy of refresh access token-")

# wait for 50minutes 50*60 seconds
time.sleep(5)
# just a delay for first refresh request
# after then thread itself runs in background after 50minutes itself
refreshToken()



# -----------------------------------------------------------------------------------
# db operations
# -----------------------------------------------------------------------------------

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test_export_genius_2',
                                         user='dubeyji',
                                         password='password')
    print('\n\n--connection successful--\n\n')
    logging.info(' --connection successful at \'{}\' --'.format(time.ctime()))

        # change to 10*60 -- 10 minute wait
        # TO-DO could make a variable for 24hr/10 minutes -- when 0 stop the execution

    while True:
        leadsDataToPush = '' 
        '''
            let say shift ends at 19:00 7pm so kill process at time 19:00:00
            (example)
        '''
        if aDate.strftime('%Y-%m-%d %H:%M:%S')== exampleDate+" 19:00:00":
            print("shift ended thank you")
            break

        logRecordVar = ''
        # dd/mm/YY H:M:S
        # this keeps running forever
        aDate = printTimeInterval2(aDate)
        
        # either add a delay here or use the delay in printTimeInterval2
        # using the time intervalfunction delay for now

        # if connection.is_connected():
        #     db_Info = connection.get_server_info()
        #     print("Connected to MySQL Server version ", db_Info)

        for_dateTime = leads_Query_withTimestamp
        print("running query for ",for_dateTime[-73:])
        # last 73 characters
        cursor = connection.cursor()
        result = cursor.execute(for_dateTime)
        leadsOutput = cursor.fetchall()
        outPut = leadsOutput[0]
        if outPut[0]==None:
            # print("-> no records inserted "+for_dateTime[-60:])
            logRecordVar = '-> no records created {}'.format(for_dateTime[-56:])
            logging.info(logRecordVar)
        else:
            newLeads = ''
            leadsJson = None
            print('-'*50)
            newLeads = outPut[0]
            print("\n\n\n-> query output  at {} \n\n\n: {}".format(time.ctime(),newLeads))
            # print("\n\ntype -> ",type(newLeads),len(newLeads))
            leadsJson = json.loads(newLeads)
            '''
                {
                    "data" : [
                        {record},{record},{record}
                    ]
                }
            '''
            # print('1. ',leadsJson,'\n\n2. ',leadsJson['data'],'\n\n3. ',len(leadsJson['data']))
            logRecordVar = '-> {} records created {}'.format(len(leadsJson['data']) , for_dateTime[-56:])
            logging.info(logRecordVar)
            print('-'*50)
            # print("calling apis to push records")
            # print("reading accessToken.json")
            # print("define payloads and headers")
            leadsDataToPush = newLeads
            # pushIntoLeads(leadsDataToPush)
            logging.info("\n\n\n\n\n>>>calling leads api at {}".format(time.ctime()))
            '''
                add try except here later
            '''
            print(">make request")
            print(">write request response to log")
            print("reading accessToken.json")
            with open(accessTokenFile,'r') as client:
                tokens = json.load(client)

            accessToken = tokens['access_token']
            url_leads = url+"Leads"
            headers = {
            'Authorization': 'Bearer '+accessToken,
            'Content-Type': 'application/json',
            }
            response = requests.request("POST", url_leads, headers=headers, data=json.dumps(leadsJson))
            # print(response.text)
            logging.info("\n ------------------------------------ \n")
            logging.info("\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),response.text))
            logging.info("\n ------------------------------------ \n")
            # print("\n\n----- pushed {} with api call -----\n\n".format(leadsJson))
            print("done")

        print('\\/\\'*25)

except Error as e:
    print("\n\nError while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        logging.info("--MySQL connection is closed at {}--".format(time.ctime()))
        sys.exit()

