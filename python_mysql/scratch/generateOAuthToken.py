import json
import requests


clientFile = 'self_client.json'
with open(clientFile,'r') as client:
        payload_oauth = json.load(client)


def generateAuthFunction(payload_dict):
    print('______________________________________')
    print("1. making api request using payload : \n",payload_dict)
    print("2. generating oauth token")
    print("3. got response")
    print("4. writing response to oauthResponse.json")            
    # read client json

    #making the request
    files=[]
    headers = {}
    urlOAuth = "https://accounts.zoho.in/oauth/v2/token"
    response = requests.request("POST", urlOAuth, headers=headers, data=payload_dict, files=files)
    # writing reponse to oauthResponse.json
    print("\t-> response generated: \n")
    print(response.text)
    with open('accessToken.json','w',encoding='utf8') as oauthResponse:
        oauthResponse.write(response.text)
    print('______________________________________')

generateAuthFunction(payload_oauth)