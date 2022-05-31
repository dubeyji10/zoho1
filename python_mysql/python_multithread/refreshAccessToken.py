from generateAuthToken import payload_dict


global myRefreshToken , totalCalls
totalCalls = 0

with open('calls.txt','w') as callCounter:
    callCounter.write("1")

# if totalCalls  == 0 call generateOAuth else not

print('-'*100)
print("it is running in the background")
print("read the accessToken.json")
print("get other variable from generateAuthToken.py")
'''

need client id and client secret get them from last file

'''
myClientId = payload_dict['client_id']
myClientSecret = payload_dict['client_secret']

'''

need access token and refresh token read them from accessToken.json
    save refreshToken value as a variable as a safegaurd


'''
print("update the content of file every 50 minutes -- 50*60 seconds")
'''
    no need to declare varaibles since everytime file is read for access token
'''

print("making api call for refresh token")
myRefreshToken = 'READ FROM acessToken.json'
#     save refreshToken value as a variable as a safegaurd
payloadRefresh={
    'client_id': myClientId,
    'client_secret': myClientSecret,
    'refresh_token': myRefreshToken,
    'grant_type': 'refresh_token'
}
print("after getting reponse overwriting the sameAccessToken.json file for updating accessToken with latest value")
'''

    output is like this
    {
    "access_token": "1000.003cb836bf1b02e4195419dbd8536b42.7692b6be1044b99b97f21f8e1b37677a",
    "api_domain": "https://www.zohoapis.in",
    "token_type": "Bearer",
    "expires_in": 3600
    }

'''

print("\n-- before making an API request always read from the file first -- \n")
print("-> refresh token is : ",myRefreshToken)
print('-'*100)

def refreshTokenFunction():
    print("______________ refresh ________________")
    print("1. waiting for 50 mintes - 50*60 seconds")
    print("2. making refresh token request with payload : \n",payloadRefresh)
    print("3. writing the output to accessToken.json")
    print("NOTE -> always read accessToken from the file before making api call")
    # print(" in refreshAccessToken totalCalls  so far --- ",totalCalls)

    # note : now accessToken.json doesnt have refresh_token key item
    # but it saved as a varibale already
    # so it should escape the issue
    print("______________ refreshed ________________")
    return
    
if __name__=="__main__":
    refreshTokenFunction()