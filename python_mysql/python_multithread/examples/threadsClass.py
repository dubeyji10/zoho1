'''
Overriding run() method in a subclass of threading.Thread.
'''

import threading
import time

'''

alternate see threads1.py

'''
class myCustomThread(threading.Thread):
    def __init__(self):
        self.i = 0

    def run(self):
        print("Waiting for 3 seconds")
        time.sleep(3)
        print("this is custom run for custom thread class,run = {}".format(i))
        self.i+=1
        # return super().run()
        # super().run()

for i in range(3):
    t = myCustomThread()
    t.run()