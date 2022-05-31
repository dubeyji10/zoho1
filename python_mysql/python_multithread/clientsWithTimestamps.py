import mysql.connector
from mysql.connector import Error
from datetime import date, time, datetime ,timedelta
import time



fileName = '2015-01-02'

'''

for generating payloads - data to be inserted in APIs - with timestamps

- a difference of 15 minutes

'''

# today = ''

exampleDate = '2015-01-02'
global clients_Query

with open('clients/clientsQuery.txt', 'r') as file:
    data = file.read()
    clients_Query = data.rstrip()


print("running for leads - query : \n",clients_Query)
clients_Query_withTimestamp = ''

# exampleDate
aDate = datetime(2015,1,2,12,30)
# for example start datetime operations at 12:30 pm

# for example going back in time -- 
# capital H,M,S - 12 format 
# 


def printTimeInterval2(dateTimeObject):
    global clients_Query_withTimestamp
    print("waiting for 10 minutes")
    time.sleep(10)
    # after 10 seconds later change it to 60*10 -- 10 minutes

    '''
    
    pass the datetime object

    wait for 10 minutes 
    query all records in the last 10 minutes

    '''
    # now = datetime.now()
    dt_string = dateTimeObject.strftime('%Y-%m-%d %H:%M:%S ')
    # print("now \t:", dt_string)
    diff = dateTimeObject + timedelta(minutes=10) 
    dateTimeObject = diff
    dt_string_diff = diff.strftime('%Y-%m-%d %H:%M:%S ')
    # print("10 minutes ago : ",dt_string_diff)
    # print("--> timestamp for difference  = {} and {} ".format(dt_string,dt_string_diff))
    # print("run this query :\n\n ")
    # print("updated leads query with timestamp")
    clients_Query_withTimestamp = clients_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    # print("\n\n\n\n")
    return diff



try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test_export_genius_2',
                                         user='dubeyji',
                                         password='password')

    print('\n\n--connection successful--\n\n')

        # change to 10*60 -- 10 minute wait
        # TO-DO could make a variable for 24hr/10 minutes -- when 0 stop the execution
    while True:
        # dd/mm/YY H:M:S
        # this keeps running forever
        aDate = printTimeInterval2(aDate)
        # if connection.is_connected():
        #     db_Info = connection.get_server_info()
        #     print("Connected to MySQL Server version ", db_Info)

        for_dateTime = clients_Query_withTimestamp
        print("run this query  : \n\n\n",for_dateTime[-73:])
        # last 73 characters
        cursor = connection.cursor()
        result = cursor.execute(for_dateTime)
        clientsOutput = cursor.fetchall()
        outPut = clientsOutput[0]
        print('-'*50)
        print("-> query output  : \n\n",outPut[0])
        print("\n\ntype -> ",type(outPut[0]),len(outPut))
        print('-'*50)
        print('\\/'*25)

except Error as e:
    print("\n\nError while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
