import requests
import json

url = "https://www.zohoapis.in/crm/v2/invoice_items"

payload = json.dumps({
  "data": [
    {
      "Name": "00000000000000000003",
      "Total_Months": 2,
      "$currency_symbol": "₹",
      "Query": "python request a sample query",
      "Data_Type": "sent from python request just a sample data type",
      "Mode_Of_Delivery": "post"
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
