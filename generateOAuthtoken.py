import requests

url = "https://accounts.zoho.in/oauth/v2/token"

payload={
    'client_id': '1000.UCYPYQ50YXV3010I5QA6LXH0TCB3WN',
    'client_secret': 'da610c19c559e2af6761d4a8f08b26835ff22916b8',
    'code': '1000.354fbdf1238d6d9cbbf298c98c67ca08.7923cc6c2f5f46047b4031cd226e9741',
    'grant_type': 'authorization_code'
}

files=[

]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)

'''


output like this


{
    "access_token": "1000.a5e4d143279af05c6fc51cd766d18af5.e06b7a25827a2f9d571135f4df8f85d6",
    "refresh_token": "1000.3313454f290ad37257f394ae17d3201b.eb03f9738e0a32176525d2021da94d54",
    "api_domain": "https://www.zohoapis.in",
    "token_type": "Bearer",
    "expires_in": 3600
}


'''
