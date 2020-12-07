import time
import serial_cross_module_test as scmt

try:
    #scmt.serialcomm = serial.Serial('/dev/ttyUSB0', 9600) ##   /dev/tty  usb/acm_n
    scmt.serialcomm.timeout = 1
except:
    print('Please check the port')

while True:

    i = input("Enter Input: ").strip()

    if i == "Done":

        print('finished')

        break

    scmt.serialcomm.write(i.encode())

    time.sleep(1.5)

    print(scmt.serialcomm.readline())

scmt.serialcomm.close()
