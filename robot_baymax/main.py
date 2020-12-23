#!/usr/bin/env python3
"""
Team 3 main.py

Starts all threads
"""

#imports
from alexa_w_websocket.alexa_w_all_to_one import *
import threading
import time

#main
if __name__ == '__main__':
    
    Connected_Chat()

    alexa_thread = threading.Thread(target=app.run)
    alexa_thread.daemon = True
    chat_thread = threading.Thread(target=chatting)

    all_threads = []
    all_threads.append(chat_thread)

    alexa_thread.start()

    print("\nAlexa is now enabled!\n")
    import time
    time.sleep(1)

    for thread in all_threads:
        thread.start()

    for thread in all_threads:
        thread.join
    

