import requests
import json

global accessToken


'''


refresh token response 

{
    "access_token": "1000.34e2de1f0a8582208902e047770c1556.f18b6140ebe6cacdc911abb59f5385a6",
    "api_domain": "https://www.zohoapis.in",
    "token_type": "Bearer",
    "expires_in": 3600
}


'''

urlRefresh = "https://accounts.zoho.in/oauth/v2/token?"
urlGenerate =  "https://accounts.zoho.in/oauth/v2/token"

files=[]
headers = {}

#  or just read from the self_clients.json
'''
data = json.load(file)
'''
fileName = './self_client.json'
# /home/dubeyji/Desktop/zoho1/python_mysql/alter/utils/self_client.json
with open(fileName,'r') as client:
    payload = json.load(client)


def generateAccessTokens():
    print('>payload : \n',payload)
    print('>making post request to create access token and refresh token')
    response = requests.request("POST", urlGenerate, headers=headers, data=payload, files=files)
    print('>saving response to oauthResponse.json')
    # with open('oauthResponse.json','w',encoding='utf8') as oauthResponse:
        # oauthResponse.write(response.text)
    print('>a copy in accessToken.json')

    # with open('accessToken.json','w',encoding='utf8') as oauthResponse:
    #     oauthResponse.write(response.text)
    print('______________________________________')

    return response
'''
first call generateAccessTokens()
'''
def refreshTokens():
    payloadRefresh={
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'refresh_token': 'your-refresh-token',
        'grant_type': 'refresh_token'
        }

    accessToken_1 = 'oauthResponse.json'
    with open(accessToken_1,'r') as t:
        OauthResponse = json.load(t)

    payloadRefresh['client_id'] = payload['client_id']
    payloadRefresh['client_secret'] = payload['client_secret']
    payloadRefresh['refresh_token'] = OauthResponse['refresh_token']
    print("payload for refreshing access token : ",payloadRefresh)

    print('refreshing access tokens')
    response = requests.request("POST", urlRefresh, headers=headers, data=payloadRefresh, files=files)
    
    # with open('accessToken.json','w',encoding='utf8') as refreshResponse:
        # refreshResponse.write(response.text)

    print('token refreshed and saved in accessToken.json')
    return response


'''

write to access_token.json every 40minute by calling refreshTokens()

'''
