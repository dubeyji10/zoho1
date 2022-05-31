import requests
import pprint
import json
'''
    Note : add https:// to the url it wont work without it
    and for indian region use .in for accounts-domain(or accounts-url)
    , and for api-domain    
    to get conversation from zoho crm

'''
url = "https://www.zohoapis.in/crm/v2/conversation"

payload={}
# try headers without Cookie
# headers = {
#   'Authorization': 'Bearer 1000.a5e4d143279af05c6fc51cd766d18af5.e06b7a25827a2f9d571135f4df8f85d6',
#   'Cookie': '941ef25d4b=892b44adba9a263d20d457c5776a03e2'
# }

headers = {
  'Authorization': 'Bearer 1000.a5e4d143279af05c6fc51cd766d18af5.e06b7a25827a2f9d571135f4df8f85d6'
  }
# works without Cookie
response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

# print('-'*100)
# pprint.pprint(response.json)

# print('-'*100)
# pprint.pprint(response.text)

print('\n\n')
# json.loads not json.load
print('-'*100)
pprint.pprint(json.loads(response.text))
