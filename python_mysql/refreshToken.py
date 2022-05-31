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

url = "https://accounts.zoho.in/oauth/v2/token?"

payload={
  'client_id': 'your-client-id',
  'client_secret': 'your-client-secret',
  'refresh_token': 'your-refresh-token',
  'grant_type': 'refresh_token'
}
files=[

]
headers = {}

#  or just read from the clients.json
'''
data = json.load(file)
'''
fileName = 'self_client.json'

# with open(fileName,'r') as client:
#     payload = json.load(client)

print("payload : ",payload)


response = requests.request("POST", url, headers=headers, data=payload, files=files)
print(response.text)

'''

write to access_token.json every 50minute

'''
