import serial

serialcomm = serial.Serial('/dev/ttyUSB0', 9600) ##   /dev/tty  usb/acm_n
#i = "1 Left 1"
#serialcomm.write(i.encode())
#serialcomm.write("1 Forward 1".encode())
#print(serialcomm.readline().decode())
#serialcomm.close()