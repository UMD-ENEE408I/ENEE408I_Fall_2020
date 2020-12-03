# Simple program to read and plot data from the Arduino serial port
import numpy as np
import serial
from PlotData import PlotData # Function in a local file

ser = serial.Serial("/dev/ttyUSB0", 9600) # Linux port, check this for your setup
ser.flushInput()
numValues=10
x = np.empty(shape=numValues, dtype=float) # initialize empty array
# Check the indents in your code. 
for k in range(numValues): 
    linein = ser.readline()
    if linein==b'\x00\n': # Not sure why this doesn't convert, crashes here sometimes
        linein=0
    xf=float(linein) # Convert to a floating point variable
    x[k]=xf
print(x)
PlotData(x)
