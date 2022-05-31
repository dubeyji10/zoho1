from fileinput import filename
import mysql.connector
from mysql.connector import Error
import json
from datetime import date, time, datetime

print("trying to connect to database")

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
                    `clients`.`company_name`,
                    'website',
                    `clients`.`website`,
                    'contact_person1',
                    `clients`.`contact_person1`,
                    'contact_person2',
                    `clients`.`contact_person2`,
                    'mobile_no1',
                    `clients`.`mobile_no1`,
                    'designation',
                    `clients`.`designation`,
                    'company_grade',
                    `clients`.`company_grade`,
                    'mobile_no2',
                    `clients`.`mobile_no2`,
                    'last_conversation',
                    `clients`.`last_conversation`,
                    'user_id',
                    `clients`.`user_id`,
                    'local_id',
                    `clients`.`id`,
                    'phonecode',
                    `clients`.`phonecode`,
                    'Country',
                    `clients`.`Country`,
                    'phone_no',(
                        select
                        case
                            when ifnull(`clients`.`phone_no`, '') <> 0 then `clients`.`phone_no`
                            else ''
                        end
                    ),
                    'last_mail_on',
                    concat(
                        concat(
                        replace(
                            date_format(`clients`.`last_mail_on`, '%Y-%m-%d %T'),
                            ' ',
                            'T'
                        ),
                        '+05:30'
                        )
                    ),
                    'last_sms_on',
                    concat(
                        concat(
                        replace(
                            date_format(`clients`.`last_sms_on`, '%Y-%m-%d %T'),
                            ' ',
                            'T'
                        ),
                        '+05:30'
                        )
                    ),
                    'added_on',
                    concat(
                        concat(
                        replace(
                            date_format(`clients`.`added_on`, '%Y-%m-%d %T'),
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
            ) AS `Name_exp_1`
            from
            `clients` 
        """
        for_date = mysql_SELECT_JSON_Query + " WHERE cast(`added_on` as date) = '2015-01-07' "

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

        fileName = 'clients_4_' + str(date.today())+".json"
        with open(fileName,'w',encoding='utf8') as outFile:
            outFile.write(outPut[0])

        print("\n\n->done check file : ",fileName)

        # print("\n\nPrinting each row")
        # for row in clients_table:
        #     print(" id = ", row[0], )
        #     print("Contact Person 1 = ", row[1])
        #     print("Contact Person 2 = ", row[2])
        #     print("company_name  = ", row[3], "\n")

except Error as e:
    print("\n\nError while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
