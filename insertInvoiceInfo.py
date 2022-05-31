import requests
import json

url = "https://www.zohoapis.in/crm/v2/invoice_info"

payload = json.dumps({
  "data": [
    {
      "Name": "270924000000373001",
      "Email":"a_test_mail@example.com",
      "Address": "7th address of client python request",
      "City": "West Hampshire",
      "State": "New Hapmshire",
      "Tel_No": "4422434120",
      "amount_recieved": "61011.78",
      "data_detail": "6th data details here for entry from python",
      "invoice_of": "client 6",
      "payment_detail": "6th write payment details here from python client",
      "sale_amount": 61144.25,
      "tds_percentage": 5
    }
  ],
  "trigger": [
    "approval",
    "workflow",
    "blueprint"
  ]
})
headers = {
  'Authorization': 'Bearer 1000.28ce3327e05adb1c48ad0452cd6a89e3.9c7b45ec8bf904ee1ba8ac2b2973454d',
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
