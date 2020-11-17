#!/usr/bin/env python3
# Allows Alexa to command the Balboa to stand up or fall down
# Derived from examples in the Flask-Ask repo: https://github.com/johnwheeler/flask-ask

import serial

from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('StandUp')
def stand_up():
    speech_text = 'Muscle Boy says its my time to shine'
    #ser.write(b'b')
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('LayDown')
def law_down():
    speech_text = 'Muscle Boy says my batteries were getting low anyway'
   	#ser.write(b'f')
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Forward')
def move_f():
    speech_text = 'Muscle Boy goes forward'
    #ser.write('Forward'.encode())
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Backward')
def move_b():
    speech_text = 'Muscle Boy goes backward'
    #ser.write('Backward'.encode())
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Left')
def move_l():
    speech_text = 'Muscle Boy turns left'
    #ser.write('Left'.encode())
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Right')
def move_r():
    speech_text = 'Muscle Boy turns right'
    #ser.write('Right'.encode())
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Stop')
def stop():
    speech_text = 'Muscle Boy will stop'
    #ser.write('Stop'.encode())
    return statement(speech_text).simple_card('Muscles', speech_text)

if __name__ == '__main__':
    #ser = serial.Serial('/dev/ttyUSB0', 9600)
    app.run()
