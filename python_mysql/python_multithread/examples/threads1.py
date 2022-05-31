'''
Overriding run() method in a subclass of threading.Thread.
'''

import threading
import time

class myCustomThread(threading.Thread):
    i=0
    
    @classmethod
    def update(self, i):
        self.i += 1
    def run(self):
        print("Waiting for 3 seconds")
        time.sleep(3)
        print("this is custom run for custom thread class,run = {}".format(i))
        self.update(i)
        # return super().run()
        # super().run()

for i in range(3):
    t = myCustomThread()
    t.run()