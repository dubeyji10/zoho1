from datetime import date, time, datetime ,timedelta
import time

print("date time loop")

'''

remember to add shebang before cron job or any automation


'''
# def datetime_range(start, end, delta):
#     current = start
#     while current < end:
#         yield current
#         current += delta

# dts = [dt.strftime('%Y-%m-%d %H:%M:%S ') for dt in 
#        datetime_range(datetime(2016, 9, 1, 7), datetime(2016, 9, 1, 9+12), 
#        timedelta(minutes=15))]

# print(dts)

print(date.today())
# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime('%Y-%m-%d %H:%M:%S ')

print("now =>", dt_string)
diff = datetime.now() - timedelta(minutes=15) 
dt_string_diff = diff.strftime('%Y-%m-%d %H:%M:%S ')
print(dt_string_diff)

print('-'*100)

def printTimeInterval():
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S ')
    print("now \t:", dt_string)
    diff = datetime.now() - timedelta(minutes=10) 
    dt_string_diff = diff.strftime('%Y-%m-%d %H:%M:%S ')
    print("10 minutes ago : ",dt_string_diff)
    time.sleep(10)


#  a date

'''

will extract data in the last 10 minutes 
for just example's sake using time.sleep(10) seconds to print time difference 

'''

aDate = datetime(2015, 8, 1, 7)


def printTimeInterval2(dateTimeObject):
    '''
    
    pass the datetime object

    '''
    # now = datetime.now()
    dt_string = dateTimeObject.strftime('%Y-%m-%d %H:%M:%S ')
    print("now \t:", dt_string)
    diff = dateTimeObject - timedelta(minutes=10) 
    dateTimeObject = diff
    dt_string_diff = diff.strftime('%Y-%m-%d %H:%M:%S ')
    print("10 minutes ago : ",dt_string_diff)
    time.sleep(10)
    return diff

while True:
    # dd/mm/YY H:M:S
    aDate = printTimeInterval2(aDate)
    print('-'*25)

