import serial
import time
import serial_cross_module_test

try:
    serialcomm = serial.Serial('/dev/ttyUSB0', 9600) ##   /dev/tty  usb/acm_n
    serialcomm.timeout = 1
except:
    print('Please check the port')

while True:

    i = input("Enter Input: ").strip()

    if i == "Done":

        print('finished')

        break

    serialcomm.write(i.encode())

    time.sleep(1.5)

    print(serialcomm.readline())

serialcomm.close()