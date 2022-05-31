from pprint import pprint
import requests
import json

'''

  in payload data
  try            
  "Layout": {
                "name": "LeadEXportGenius",
                "id": "270924000000000167"
            },

'''
url = "https://www.zohoapis.in/crm/v2/Leads"

# trying to insert a lead using api and requests

payload = json.dumps({
  "data": [
    {
      "Company": "Test Company",
      "First_Name":"Samplefirstname",
      "Last_Name":"Lastname",
      "Lead_Source": "advertisement 1",
      "Email": "newcrmapi@zoho.com",
      "Title": "a sample title",
      "Mobile": "9292131399",
      "Skype_ID": "@iamskype2"
    }
  ],
  "trigger": [
    "approval",
    "workflow",
    "blueprint"
  ]
})
headers = {
  'Authorization': 'Bearer 1000.e36b9f42b557f961c1161eacf75eb069.a4aa6f20cdd246f28b77eaa8454351cd',
  'Content-Type': 'application/json',
  'Cookie': '941ef25d4b=12f28b642b9006c93f19042168484cf1'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

