import requests

#16 may
#create new client for new tokens
#try new scopes for insert

url = "https://accounts.zoho.in/oauth/v2/token?"

payload={'client_id': '1000.UCYPYQ50YXV3010I5QA6LXH0TCB3WN',
'client_secret': 'da610c19c559e2af6761d4a8f08b26835ff22916b8',
'refresh_token': '1000.b9fd4a338cd6fd0b81d9cd1d265944f3.f7189169e2885c2aad5f4985f8008e81',
'grant_type': 'refresh_token'}
files=[

]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
