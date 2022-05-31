import requests
import json

global accessToken

url = "https://accounts.zoho.in/oauth/v2/token"
payload = None

#  or just read from the clients.json
'''
data = json.load(file)
'''
fileName = 'self_client.json'

with open(fileName,'r') as client:
    payload = json.load(client)

print("payload : ",payload)
# payload={
#     'client_id': '1000.UCYPYQ50YXV3010I5QA6LXH0TCB3WN',
#     'client_secret': 'da610c19c559e2af6761d4a8f08b26835ff22916b8',
#     'code': '1000.354fbdf1238d6d9cbbf298c98c67ca08.7923cc6c2f5f46047b4031cd226e9741',
#     'grant_type': 'authorization_code'
# }
print('-'*50)
for keys in payload:
    print(keys , ":" , payload[keys])
print('-'*50)


files=[

]
headers = {}

'''

make request

'''
# response = requests.request("POST", url, headers=headers, data=payload, files=files)
# print(response.text)

'''

write access_token to access_token.txt

'''

accessToken = "asdkaskdksadnasdl"

print(accessToken)

#  python generateOauthToken.py
