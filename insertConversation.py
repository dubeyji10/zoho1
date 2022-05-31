import requests
import json

url = "https://www.zohoapis.in/crm/v2/conversation"

payload = json.dumps({
  "data": [
    {
      "msg": "Third this is for testing whether custom module is created or not",
      "Owner": {
        "name": "Jitendra Kumar",
        "id": "270924000000373001",
        "email": "jitendra.seo@exportgenius.in"
      },
      "$currency_symbol": "₹",
      "$field_states": None,
      "with_email": "thisis3rd@mail.com",
      "$review_process": {
        "approve": False,
        "reject": False,
        "resubmit": False
      },
      "Name": "third sample conversation",
      "Last_Activity_Time": None,
      "Record_Image": None,
      "$review": None,
      "$state": "save",
      "Unsubscribed_Mode": None,
      "$process_flow": False,
      "$approved": True,
      "$approval": {
        "delegate": False,
        "approve": False,
        "reject": False,
        "resubmit": False
      },
      "s_n": 99988833345,
      "Created_Time": "",
      "Unsubscribed_Time": None,
      "$editable": True,
      "followup_on": "",
      "$orchestration": False,
      "user_id": "270924000000373001",
      "$in_merge": False,
      "Tag": [],
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
  'Authorization': 'Bearer 1000.de072a638ca34f11d5813f2f0a085d99.2db6d00df4bccb40c2300b0625d219f2',
  'Content-Type': 'application/json',
  'Cookie': '941ef25d4b=e2b0bd05a565a5520acb39d78a2c1001; _zcsr_tmp=92848ca1-873b-4d11-8046-a8aefbca09f0; crmcsr=92848ca1-873b-4d11-8046-a8aefbca09f0'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
