import threading
import time
def f():
    print('Thread function\n')
    return
for i in range(3):
    t = threading.Thread(target=f)
    t.start()
    time.sleep(5)
    
print("while this works ")
print('-'*100)