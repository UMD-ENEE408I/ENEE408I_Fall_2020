#!/usr/bin/env python3
# Allows Alexa to command the Balboa to stand up or fall down
# Derived from examples in the Flask-Ask repo: https://github.com/johnwheeler/flask-ask

import serial

from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('forward_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def move_forward(duration, decimal):
    print(str(duration) + ' ' + str(decimal))
    divisor = 10
    while(int(decimal) > divisor):
    	divisor *= 10
    time = float(duration)+ float(decimal)/float(divisor)
    speech_text = 'Self Made moves foward for {} seconds'.format(time);
    print(time)
    ser.write('1 Forward {}'.format(duration).encode())
    print(ser.readline().decode())
    return statement(speech_text).simple_card('Muscles', speech_text)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    app.run()
