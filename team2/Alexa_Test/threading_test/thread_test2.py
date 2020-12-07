import threading
import thread_test as tt1
import time

if __name__ == '__main__':
    tt1_thread = threading.Thread(target=tt1.printf)
    tt1_thread.start()
    time.sleep(2)
    tt1.name = 'Mark'
    time.sleep(2)