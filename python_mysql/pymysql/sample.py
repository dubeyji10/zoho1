import pymysql
import pymysql.cursors
from datetime import date, datetime ,timedelta
import time



leads_Query = ''
clients_Query = ''
conversation_Query = ''
invoiceItems_Query = ''
invoiceInfo_Query = ''

with open('leads/leadsQuery.txt', 'r') as file:
    data = file.read()
    leads_Query += data.rstrip()
with open('clients/clientsQuery.txt', 'r') as file:
    data = file.read()
    clients_Query += data.rstrip()
with open('conversation/conversationQuery.txt', 'r') as file:
    data = file.read()
    conversation_Query += data.rstrip()
with open('invoice_items/invoice_itemsQuery.txt', 'r') as file:
    data = file.read()
    invoiceItems_Query += data.rstrip()
with open('invoice_info/invoice_infoQuery.txt', 'r') as file:
    data = file.read()
    invoiceInfo_Query += data.rstrip()


aDate = datetime(2015,1,10,10,00)
# shiftEndAt = datetime(2015,1,10,20,00)


def updateTime(dateTimeObject):
    global aDate
    print("waiting for 10 minutes - all records inserted in next ten minutes to be considered")
    time.sleep(10) 
    # 10 seconds --- now ---
    # after 10 seconds later change it to 60*10 -- 10 minutes
    # or just remove it since time delta is calculate after 10 minute wait alread no need to sleep here
    # dont remove delay is not added in infinite loop for now use delay here
    '''
    
    pass the datetime object

    wait for 10 minutes 
    query all records in the last 10 minutes

    '''
    dt_string = dateTimeObject.strftime('%Y-%m-%d %H:%M:%S')
    diff = dateTimeObject + timedelta(minutes=10) 
    dateTimeObject = diff
    dt_string_diff = diff.strftime('%Y-%m-%d %H:%M:%S')

    leads_Query_withTimestamp = leads_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    clients_Query_withTimestamp = clients_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    conversation_Query_withTimestamp = conversation_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    invoiceInfo_withTimestamp = invoiceInfo_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    invoiceItems_withTimestamp = invoiceItems_Query+" WHERE added_on between '{}' and '{}' ".format(dt_string,dt_string_diff)
    UpdatedQueriesList = [leads_Query_withTimestamp , clients_Query_withTimestamp ,
                conversation_Query_withTimestamp , invoiceInfo_withTimestamp,
                invoiceItems_withTimestamp
                ]
    return [diff , UpdatedQueriesList]





# Connect to the database
connection = pymysql.connect(host='localhost',
                            database='test_export_genius_2',
                            user='dubeyji',
                            password='password',
                            cursorclass=pymysql.cursors.DictCursor)

with connection:

    [aDate , queriesList] = updateTime(aDate) 
    print("now aDate var : {}".format(aDate))
    for i in queriesList:
        with connection.cursor() as cursor:
            # Read a single record
            sql = i
            print('>>running : ',i[-100:])
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)