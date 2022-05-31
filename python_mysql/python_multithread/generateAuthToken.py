
'''
    generate oauth  for access token and refresh tokens

'''
'''
    self_client.json put in the same directory
    {
    "scope": [
        "ZohoCRM.modules.ALL",
        "ZohoCRM.org.ALL",
        "ZohoCRM.modules.custom.all",
        "ZohoCRM.users.all",
        "ZohoCRM.org.all",
        "ZohoCRM.settings.all"
    ],
    "expiry_time": 1653655229125, - - -this is epoch - Date and time (GMT): Saturday, 28 May 2022 7:35:38 AM
    "client_id": "1000.UCYPYQ50YXV3010I5QA6LXH0TCB3WN",
    "client_secret": "da610c19c559e2af6761d4a8f08b26835ff22916b8",
    "code": "1000.d5c5dc08afa97101f595a4b11a8935f3.1869eb98f86d95e18a1a812d4c7513de",
    "grant_type": "authorization_code"
}

for oauth generation     "grant_type": "authorization_code"

'''

global payload_dict
payload_dict = {

    "client_id" : "your-client-id",
    "client_secret" : "your-client-secret" ,  
    "grant_type": "authorization_code",
    "code": "your-code-from-api-console",
    "grant_type": "authorization_code"

} 
print("reading self_client.json")
'''
    output like this write to accessToken.json
    save refreshToken value as a variable as a safegaurd


{
    "access_token": "1000.a5e4d143279af05c6fc51cd766d18af5.e06b7a25827a2f9d571135f4df8f85d6",
    "refresh_token": "1000.3313454f290ad37257f394ae17d3201b.eb03f9738e0a32176525d2021da94d54",
    "api_domain": "https://www.zohoapis.in",
    "token_type": "Bearer",
    "expires_in": 3600
}

'''

def generateAuthFunction():
    global payload_dict
    print('______________________________________')
    print("1. making api request using payload : \n",payload_dict)
    print("2. generating oauth token")
    print("3. got response")
    print("4. writing response to accessToken.json")
    print('- function call complete -')
    print('______________________________________')
    # return
    
print('-'*100)


if __name__=="__main__":
    generateAuthFunction()