import imp
import threading
import time
from datetime import date, datetime ,timedelta
import requests
import json
import pprint
import os
import shutil
import sys
import logging

global totalCalls_toDB
totalCalls_toDB = 0
# for logging
now = datetime.now()
fileName = now.strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename="logs/"+fileName+"_threads_1"+".log", level=logging.INFO)



'''
just a temp variable to exit script
say now totalCycles = 10
sys.exit()
'''

'''
 global variables

globvar = 0

def set_globvar_to_one():
    global globvar    # Needed to modify global copy of globvar
    globvar = 1

def print_globvar():
    print(globvar)     # No need for global declaration to read value of globvar

set_globvar_to_one()
print_globvar()       # Prints 1


'''

print("1. conection to db is established")
logging.info(' --connection successful at \'{}\' --'.format(time.ctime()))



totalCalls = 0

global payload_oauth
# read from self_client.json
payload_oauth = {

    "client_id" : "your-client-id",
    "client_secret" : "your-client-secret" ,  
    "grant_type": "authorization_code",
    "code": "your-code-from-api-console",
    "grant_type": "authorization_code"

} 

# first part oauth
def generateAuthFunction(payload_dict):
    print('______________________________________')
    print("1. making api request using payload : \n",payload_dict)
    print("2. generating oauth token")
    print("3. got response")
    print("4. writing response to oauthResponse.json")            
    logging.info(" oauth generation at {} ".format(time.ctime()))
    # read client json
    # fileName = 'self_client.json'
    # with open(fileName,'r') as client:
    #     payload = json.load(client)

    #making the request
    # files=[]
    # headers = {}
    # response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # writing reponse to oauthResponse.json
    # print("\t-> response generated: \n")
    
    # pprint.pprint(response.text)
    # with open('oauthResponse.json','w',encoding='utf8') as oauthResponse:
    #     oauthResponse.write(response.text)
    print('______________________________________')
    logging.info("\n --------------------------------------------------- \n")
    logging.info("\n --------- response to oauth request ---------------- \n")
    logging.info("\n --------------------------------------------------- \n")
    
    # return
    
# with open('oauthResponse.json','r') as client:
#     refreshTokenVar = json.load(client)
# # myRefreshToken = refreshTokenVar['refresh_token']

# copy contents of oauthresponse to accesstoken.json
# since access Token first is used before refreshing
# after that refreshtoken is stored in a variable and used



def refreshToken():
    if totalCalls_toDB==20:
        # logging.info(" -- disconnected db at {} -- ".format(time.ctime()))
        logging.info("-- done for today -- ")
        logging.info("-- stopped generating refresh tokens at {}--".format(time.ctime()))
        print("shift ended thank you closing the db connection ,kill the script")
        sys.exit()

    global totalCalls
    # url = "https://accounts.zoho.in/oauth/v2/token?"
    # global accessTokenFile
    # payload = None
    print("->refreshing the access tokens")
    logging.info(" -> refreshing tokens at {} ".format(time.ctime()))

    # with open('self_client.json','r') as client:
    #     payload = json.load(client)
    print("1. creating payload for refresh request")
    # myClientID = payload['client_id']
    # myClientSecret = payload['client_secret']

    # read oauthResponse.json for refresh and access token 
    print("\t 1.1 read the written oauthResponse.json for access token and refresh token")
    # with open('oauthResponse.json','r') as client:
    #     refreshTokenVar = json.load(client)
    # myRefreshToken = refreshTokenVar['refresh_token']

    # print("client id : {} \n client secret : {} \n refresh token : {}".format(myClientID,
    # myClientSecret,myRefreshToken))
    print("2. thread starts ")
    # at every 25 seconds thread runs
    logging.info(" writing refresh token request response at {} ".format(time.ctime()))
    timer = threading.Timer(25, refreshToken) # # Call `print_hello` in 25 seconds.
    timer.start()
    print("3. make api calls \n make changes in access_token.json")
    # files=[]
    # headers = {}

    # payloadRefresh={
    # 'client_id': myClientID,
    # 'client_secret': myClientSecret,
    # 'refresh_token': myRefreshToken,
    # 'grant_type': 'refresh_token'
    # }

    # refreshResponse = requests.request("POST", url, headers=headers, data=payloadRefresh, files=files)
    # print("\t 3.1 response to refresh token request : \n")
    # print("response : ---- \n\n",refreshResponse,'\n\n')
    # pprint.pprint(refreshResponse.text)
    print("4. writing response to accessToken.json ")
    logging.info("\n --------------------------------------------------- \n")
    logging.info("\n --------- response to refresh request ---------------- \n")
    logging.info("\n --------------------------------------------------- \n")

    # with open(accessTokenFile,'w') as refresh:
    #     refresh.write(refreshResponse.text)
    print("-done-")
    totalCalls+=1
    print('|-- total calls {} --|'.format(totalCalls))
    print('\\/'*25)


# call generateoauth
generateAuthFunction(payload_oauth)

src="oauthResponse.json"
dst="accessToken.json"
print("-> now src = {} exists and can copy as dst = {}".format(src , dst))
# write refresh token response  - access token in the accessToken.json
# shutil.copy(src,dst)
print("->created copy of refresh access token-")
accessTokenFile = dst

# wait for 50minutes 50*60 seconds
time.sleep(5)
refreshToken()


while True:
    if totalCalls_toDB==20:
        # logging.info(" -- disconnected db at {} -- ".format(time.ctime()))
        logging.info(" -- MySQL connection is closed at {}--".format(time.ctime()))
        sys.exit()

    totalCalls_toDB+=1
    print("this runs in background")
    print("connect to db then perfrom operations")
    print("2. fetch records for timestamp")
    print("3. if records fetched")
    logging.info("| ------------------------------------------- |")
    logging.info(" fetched records at {}".format(time.ctime()))
    print("4. read accessToken.json")
    print("5. make api request")
    logging.info(" making api request to push data at {}".format(time.ctime()))
    print("6. log the request response")
    logging.info("\n --------------------------------------------------- \n")
    logging.info("\n --- writing reponse to api --- \n")
    logging.info("\n --------------------------------------------------- \n")
    print("got back to step 2")
    logging.info("| ------------------------------------------- |")
    print("\n>>waiting for --- 15 minutes for recrods to be entered and then to perfrom operations ---\n\n")
    time.sleep(5)
    print('\\/'*25)