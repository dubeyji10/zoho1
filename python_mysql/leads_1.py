from fileinput import filename
import mysql.connector
from mysql.connector import Error
import json
from datetime import date, time, datetime
import requests

print("trying to connect to database")

'''

    Note when using time difference
    check for response to have length > 20 (say)
    only then make API call


'''

url = "https://www.zohoapis.in/crm/v2/Leads"

# url = "https://www.zohoapis.in/crm/v2/conversation"
# url = "https://www.zohoapis.in/crm/v2/clients"


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test_export_genius_2',
                                         user='dubeyji',
                                         password='password')

    print('\n\n--connection successful--\n\n')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        print('-'*50)

        mysql_SELECT_JSON_Query = """
            SELECT concat(
                '{',
                '"',
                'data',
                '"',
                ':',
                '[',
                regexp_replace(
                group_concat(
                    json_object(
                    'Name',
                    cast(`leads`.`id` as char charset utf8mb4),
                    'Last_Name',
                    '(lead)',
                    'local_id',
                    `leads`.`id`,
                    'user_id',
                    `leads`.`user_id`,
                    'client_id',
                    `leads`.`client_id`,
                    'status',
                    `leads`.`status`,
                    'requirement',
                    `leads`.`requirement`,
                    'importance',
                    `leads`.`importance`,
                    'report_type',
                    `leads`.`report_type`,
                    'source',
                    `leads`.`lead_source`,
                    'causes',
                    `leads`.`causes`,
                    'invoice_id',
                    `leads`.`invoice_id`,
                    'temp',
                    `leads`.`temp`,
                    'opening_price',
                    `leads`.`opening_price`,
                    'closing_price',
                    `leads`.`closing_price`,
                    'time_from',
                    date_format(`leads`.`time_from`, '%Y-%m-%d'),
                    'time_to',
                    date_format(`leads`.`time_to`, '%Y-%m-%d'),
                    'added_on',
                    concat(
                        concat(
                        replace(
                            date_format(`leads`.`added_on`, '%Y-%m-%d %T'),
                            ' ',
                            'T'
                        ),
                        '+05:30'
                        )
                    )
                    ) separator ','
                ),
                '(})',
                concat('}', '')
                ),
                ']',
                '}'
            ) AS `leadsJson`
            from
            `leads`
        """

        for_date = mysql_SELECT_JSON_Query + " WHERE cast(`added_on` as date) = '2015-01-08' "

        # for_date = mysql_SELECT_JSON_Query

        print("run this query  : \n\n\n",for_date)
        cursor = connection.cursor()
        result = cursor.execute(for_date)
        clients_table = cursor.fetchall()
        # print("table fetched successfully ")
        # print("output : \n\n")
        # print(clients_table)
        # print("\n\ntype -> ",type(clients_table))
        # print('.'*50)
        outPut = clients_table[0]
        # print("first output  : \n\n",outPut)
        # print("\n\ntype -> ",type(outPut),len(outPut))

        print('-'*50)
        print("final : \n\n\n")
        print("-> output  : \n\n",outPut[0])
        print("\n\ntype -> ",type(outPut[0]),len(outPut))

        # writing output to a json file
        # although it doesnt have data of today (date)
        # modify where clause when doing so

        fileName = 'leads_2' + str(date.today())+".json"
        with open(fileName,'w',encoding='utf8') as outFile:
            outFile.write(outPut[0])

        print("\n\n->done check file : ",fileName)

        # sending data through API
        headerFile = 'access_token.json'
        with open(headerFile,'r') as client:
            accessToken = json.load(client)

        print("accessToken : ",accessToken)

        ''' post request to push data into zoho crm '''
        headers = {
        'Authorization': 'Bearer ' + accessToken['access_token'],
        'Content-Type': 'application/json',
        }
        ''' read the latest access token from file and append it to header '''

        payload = outPut[0]

        # response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        # print(response.text)

        print("headers for post request : \n\n",headers)




except Error as e:
    print("\n\nError while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
