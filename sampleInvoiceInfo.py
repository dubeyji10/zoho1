import requests
import json
import pprint
'''

    fetching data from invoice info

'''
url = "https://www.zohoapis.in/crm/v2/invoice_info"

payload={}
headers = {
  'Authorization': 'Bearer 1000.23e67f3696d1507b89173a122252d4ed.19f4d0c69d5dcd79b244eab50e138368',
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
print('-'*100)
pprint.pprint(json.loads(response.text))
