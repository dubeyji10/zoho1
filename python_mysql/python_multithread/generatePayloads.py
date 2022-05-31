import mysql.connector
from mysql.connector import Error
from datetime import date, time, datetime ,timedelta
import time
import logging
import json
import sys

'''

    logging the outputs

'''
# tesing leads entered on 2015 Jan 07
# fileName = '2015-01-07'
now = datetime.now()
fileName = now.strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(filename="logs/"+fileName+"_temp_1"+".log", level=logging.INFO)

'''

for generating payloads - data to be inserted in APIs - with timestamps

- a difference of 15 minutes

'''

# today = ''

exampleDate = '2015-01-07'
# use exampledate for sysexit call

global leads_Query

with open('leads/leadsQuery.txt', 'r') as file:
    data = file.read()
    leads_Query = data.rstrip()


# print("running for leads - query : \n",leads_Query)
leads_Query_withTimestamp = ''
# --------------------------------------------------------
# 
# exampleDate
global aDate
aDate = datetime(2015,1,7,11,30)
# new datitimedifference is assigned to it
# for example start datetime operations at 11:30 am
# for example going back in time -- 
# capital H,M,S - 12 format 
# 
# --------------------------------------------------------

def printTimeInterval2(dateTimeObject):
    global leads_Query_withTimestamp
    print("waiting for 10 minutes")
    time.sleep(10)
    # after 10 seconds later change it to 60*10 -- 10 minutes

    '''
    
    pass the datetime object

    wait for 10 minutes 
    query all records in the last 10 minutes

    '''
    # now = datetime.now()
    dt_string = dateTimeObject.strftime('%Y-%m-%d %H:%M:%S')
    # print("now \t:", dt_string)
    diff = dateTimeObject + timedelta(minutes=10) 
    dateTimeObject = diff
    dt_string_diff = diff.strftime('%Y-%m-%d %H:%M:%S')
    # print("10 minutes ago : ",dt_string_diff)
    # print("--> timestamp for difference  = {} and {} ".format(dt_string,dt_string_diff))
    # print("run this query :\n\n ")
    # print("updated leads query with timestamp")
    leads_Query_withTimestamp = leads_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    # print("\n\n\n\n")
    return diff



try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test_export_genius_2',
                                         user='dubeyji',
                                         password='password')
    print('\n\n--connection successful--\n\n')
    logging.info(' --connection successful at \'{}\' --'.format(time.ctime()))

        # change to 10*60 -- 10 minute wait
        # TO-DO could make a variable for 24hr/10 minutes -- when 0 stop the execution
    while True:
                
        '''
            let say shift ends at 18:00 6pm so kill process at time 18:00:00
            (example)
        '''
        if aDate.strftime('%Y-%m-%d %H:%M:%S')== exampleDate+" 18:00:00":
            print("shift ended thank you")
            break

        logRecordVar = ''
        # dd/mm/YY H:M:S
        # this keeps running forever
        aDate = printTimeInterval2(aDate)
        # if connection.is_connected():
        #     db_Info = connection.get_server_info()
        #     print("Connected to MySQL Server version ", db_Info)

        for_dateTime = leads_Query_withTimestamp
        print("running query for ",for_dateTime[-73:])
        # last 73 characters
        cursor = connection.cursor()
        result = cursor.execute(for_dateTime)
        leadsOutput = cursor.fetchall()
        outPut = leadsOutput[0]
        if outPut[0]==None:
            # print("-> no records inserted "+for_dateTime[-60:])
            logRecordVar = '-> no records created {}'.format(for_dateTime[-56:])
            logging.info(logRecordVar)
        else:
            newLeads = ''
            leadsJson = None
            print('-'*50)
            newLeads = outPut[0]
            print("-> query output  at {} \n\n: {}".format(time.ctime(),newLeads))
            # print("\n\ntype -> ",type(newLeads),len(newLeads))
            leadsJson = json.loads(newLeads)
            '''
                {
                    "data" : [
                        {record},{record},{record}
                    ]
                }
            '''
            # print('1. ',leadsJson,'\n\n2. ',leadsJson['data'],'\n\n3. ',len(leadsJson['data']))
            logRecordVar = '-> {} records created {}'.format(len(leadsJson['data']) , for_dateTime[-56:])
            logging.info(logRecordVar)
            print('-'*50)

        print('\\/'*25)

except Error as e:
    print("\n\nError while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        logging.info("--MySQL connection is closed at {}--".format(time.ctime()))
        sys.exit()