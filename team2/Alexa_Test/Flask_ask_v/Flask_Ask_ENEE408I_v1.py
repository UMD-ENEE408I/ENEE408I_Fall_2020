#!/usr/bin/env python3
# Allows Alexa to command the Balboa to stand up or fall down
# Derived from examples in the Flask-Ask repo: https://github.com/johnwheeler/flask-ask

import serial

from flask import Flask
from flask_ask import Ask, statement
import facerec_from_webcam_faster1 as facerec

app = Flask(__name__)
ask = Ask(app, '/')

user_name = "Unknown"
default_user = "Yuchen"


@ask.intent('StandUp')
def stand_up():
    speech_text = 'Self Made says its my time to shine'
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('LayDown')
def law_down():
    speech_text = 'Self Made says my batteries were getting low anyway'
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Forward')
def move_f():
    #user_name = facerec.detect_user()
    if(user_name == default_user):
        speech_text = 'Self Made goes forward, do you like turtles?'
        ser.write('Forward'.encode())
        print(ser.readline())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Backward')
def move_b():
    #user_name = facerec.detect_user()
    if(user_name == default_user):   
        speech_text = 'Self Made goes backward, do you like turtles?'
        ser.write('Backward'.encode())
        print(ser.readline())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Left')
def move_l():
    #user_name = facerec.detect_user()
    #print(user_name + ' ' + default_user)
    if(user_name == default_user):  
        speech_text = 'Self Made turns left, do you like turtles?'
        ser.write('Left'.encode())
        print(ser.readline())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Right')
def move_r():
    #user_name = facerec.detect_user()
    if(user_name == default_user):  
        speech_text = 'Self Made turns right, do you like turtles?'
        ser.write('Right'.encode())
        print(ser.readline())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Stop')
def stop():
    speech_text = 'Self Made will stop. I am dead'
    ser.write('Stop'.encode())
    print(ser.readline())
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Self_Driving_MODE')
def self_Driving():
    if(user_name == default_user):  
        speech_text = 'Self made enters self driving mode, I am feeling more energized than ever'
        ser.write('Self_Driving'.encode())
        print(ser.readline())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Face_rec')
def face_rec():
    global user_name 
    user_name = facerec.detect_user()
    print(user_name)
    speech_text = 'You are {}'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Lock')
def lock_robot():
    global user_name
    user_name = 'Unknown'
    speech_text = 'Self Made has locked itself'
    return statement(speech_text).simple_card('Muscles', speech_text)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    app.run()
