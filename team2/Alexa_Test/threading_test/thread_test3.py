import threading
import camera_function as cf
import time

if __name__ == '__main__':
    cf_thread = threading.Thread(target=cf.run_cam)
    cf_thread.start()