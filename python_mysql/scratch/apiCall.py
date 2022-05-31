import requests
import json
# import logging
import time
from datetime import datetime

url = "https://www.zohoapis.in/crm/v2/"
# now = datetime.now()
# fileName = now.strftime('%Y_%m_%d_%H_%M_%S')
# logging.basicConfig(filename="outputs2/requests_"+fileName+"_testing_3"+".log", level=logging.INFO)
# logging.info("-- operations started at {} (test time = 2015 Jan 6 10:00) --".format(time.ctime()))

'''
sending json.dumps({"data":list_of_records})
'''
def pushInto(moduleName , payload):
    # will return responseGenerated
    # logging.info("|| calling api to insert {} at {} ||".format(moduleName,time.ctime()))
    '''
        add try except here later
    '''
    print(">make request")
    print(">write request response to log")
    print(">reading accessToken.json")
    accessTokenFile = "accessToken.json"
    with open(accessTokenFile,'r') as client:
        tokens = json.load(client)

    accessToken = tokens['access_token']
    url_module = url+moduleName
    print("url used to make api calls ->",url_module)
    headers = {
        'Authorization': 'Bearer '+accessToken,
        'Content-Type': 'application/json',
        }
    response = requests.request("POST", url_module, headers=headers, data=payload)
    # print(response.text)
    # responseText = ''
    # responseText = line+"\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),response.text)+line
    # logging.info(responseText)
    return response
