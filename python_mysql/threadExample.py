import threading
import time

tokenSamples = [i for i in range(1,101)]
counter = 0
def generateoAuthToken():
    print("generated oauth access token ")
    print("got access token , \n refresh token \n refresh the token in 3600 - before 1hr")

generateoAuthToken()


def print_hello():
    global counter
    print('-'*50)
    print('5 seconds passed refreshing token')
    timer = threading.Timer(5, print_hello) # # Call `print_hello` in 5 seconds.
    timer.start()
    print("made api calls\n made changes in access_token.json")
    tokenVal = tokenSamples[counter]
    counter+=1
    print("----> token now : ",tokenVal)

time.sleep(5)
print_hello()
# 10th - 9 tokenVal


print("read data from json create payload after every 15 minutes")