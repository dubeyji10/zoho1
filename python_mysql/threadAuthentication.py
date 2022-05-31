import threading
import time
import requests
import json
import pprint

global accessToken
url = "https://accounts.zoho.in/oauth/v2/token"
payload = None

'''
use this file for fetching the usable current access token
'''
accessTokenFile = "accessToken_refresh.json"


counter = 0
def generateoAuthToken():
    print("generating oauth access token ")
    fileName = 'self_client.json'
    with open(fileName,'r') as client:
        payload = json.load(client)
    print("->1. payload : ",payload)
    files=[
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print("->2. response : \n")
    pprint.pprint(response.text)
    with open('tempAccessToken.json','w',encoding='utf8') as accessToken:
        accessToken.write(response.text)
    print('-'*70)
    print("got access token , \n refresh token \n refresh the token in 3600 - before 1hr")

# generateoAuthToken()

'''

already called generateoAuthToken so comment for now

'''

#  or just read from the clients.json
'''
data = json.load(file)
'''


def refreshToken():
    url = "https://accounts.zoho.in/oauth/v2/token?"
    global accessTokenFile
    payload = None
    with open('self_client.json','r') as client:
        payload = json.load(client)

    myClientID = payload['client_id']
    myClientSecret = payload['client_secret']

    with open('tempAccessToken.json','r') as client:
        refreshTokenVar = json.load(client)
    myRefreshToken = refreshTokenVar['refresh_token']

    print("client id : {} \n client secret : {} \n refresh token : {}".format(myClientID,
    myClientSecret,myRefreshToken))
    print('-'*50)

    print('10 seconds passed refreshing token')
    timer = threading.Timer(5, refreshToken) # # Call `print_hello` in 5 seconds.
    timer.start()
    print("make api calls\n make changes in access_token.json")
    files=[

    ]
    headers = {}

    payloadRefresh={
    'client_id': myClientID,
    'client_secret': myClientSecret,
    'refresh_token': myRefreshToken,
    'grant_type': 'refresh_token'
    }
    files=[

    ]
    refreshResponse = requests.request("POST", url, headers=headers, data=payloadRefresh, files=files)
    print("1. response to refresh token request : \n")
    print("response : ---- \n\n",refreshResponse,'\n\n')
    pprint.pprint(refreshResponse.text)
    with open(accessTokenFile,'w') as refresh:
        refresh.write(refreshResponse.text)

time.sleep(5)
refreshToken()
# 10th - 9 tokenVal


print("read data from json create payload after every 15 minutes")