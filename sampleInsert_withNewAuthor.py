import requests
import json

'''

    in this payload has a created by field in json with neccessary fields
    so creation is done by that user

      "Created_By": {
        "name": "Rajat Gupta",
        "id": "270924000000217001",
        "email": "info@exportgenius.in"
      },

      and owner field
    "Owner": {
        "name": "Rajat Gupta",
        "id": "270924000000217001",
        "email": "info@exportgenius.in"
      },


'''

url = "https://www.zohoapis.in/crm/v2/Leads"

payload = json.dumps({
  "data": [
    {
      "Owner": {
        "name": "Rajat Gupta",
        "id": "270924000000217001",
        "email": "info@exportgenius.in"
      },
      "First_Name": "Secondexample",
      "Company": "A Test Company from python",
      "time_to": None,
      "Email": "python_code@emailaddress.in",
      "$currency_symbol": "₹",
      "$field_states": None,
      "closing_price": "102025",
      "$state": "save",
      "Unsubscribed_Mode": None,
      "$converted": False,
      "$process_flow": False,
      "Exchange_Rate": 1,
      "Currency": "INR",
      "invoice_id": None,
      "Street": None,
      "Zip_Code": "110251",
      "$approved": True,
      "$approval": {
        "delegate": False,
        "approve": False,
        "reject": False,
        "resubmit": False
      },
      "$editable": True,
      "report_type": None,
      "City": "Udaipur",
      "State": "Rajasthan",
      "Country": "India",
      "Created_By": {
        "name": "Rajat Gupta",
        "id": "270924000000217001",
        "email": "info@exportgenius.in"
      },
      "Annual_Revenue": None,
      "Secondary_Email": "thisisfrompython_request@example.com",
      "status": None,
      "Description": None,
      "Rating": None,
      "$review_process": {
        "approve": False,
        "reject": False,
        "resubmit": False
      },
      "Website": None,
      "Twitter": "testmyaccount",
      "$canvas_id": None,
      "Salutation": None,
      "Lead_Status": None,
      "Record_Image": None,
      "$review": None,
      "Skype_ID": "@askypexample2",
      "lead_source1": None,
      "Phone": "956456127",
      "causes": "This  is entry from python request",
      "Email_Opt_Out": False,
      "opening_price": "120005",
      "temp": None,
      "$converted_detail": {},
      "Unsubscribed_Time": None,
      "requirement": None,
      "Mobile": "12345689",
      "$orchestration": False,
      "Last_Name": "Example",
      "$in_merge": False,
      "Lead_Source": "adverstisement",
      "Tag": [],
      "Fax": None,
      "$approval_state": "approved"
    }
  ],
  "trigger": [
    "approval",
    "workflow",
    "blueprint"
  ]
})
headers = {
  'Authorization': 'Bearer 1000.34e2de1f0a8582208902e047770c1556.f18b6140ebe6cacdc911abb59f5385a6',
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
