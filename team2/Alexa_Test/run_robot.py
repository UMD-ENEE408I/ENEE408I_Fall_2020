#!/usr/bin/env python3
# Allows Alexa to command the Balboa to stand up or fall down
# Derived from examples in the Flask-Ask repo: https://github.com/johnwheeler/flask-ask

import serial
from flask import Flask
from flask_ask import Ask, statement
import facerec_from_webcam_faster as facerec
import threading

app = Flask(__name__)
ask = Ask(app, '/')

user_name = "Unknown"
default_user = "Yuchen"

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
    user_name = facerec.name
    speech_text = 'You are {}'.format(facerec.name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Lock')
def lock_robot():
    global user_name
    user_name = "Unknown"
    speech_text = 'Self Made has locked itself'
    return statement(speech_text).simple_card('Muscles', speech_text)


@ask.intent('forward_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def move_forward(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'Self Made moves foward for {} seconds, do you like turtles?'.format(time);
        ser.write('1 Forward {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('backward_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def move_forward(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'Self Made moves backward for {} seconds, do you like turtles?'.format(time);
        ser.write('1 Backward {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('left_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def move_forward(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'Self Made turns left for {} secondsm do you like turtles?'.format(time);
        ser.write('1 Left {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)


@ask.intent('right_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def move_forward(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'Self Made turns right for {} seconds, do you like turtles?'.format(time);
        ser.write('1 Right {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('follow_me')
def april_tag_follow():
    if(user_name == default_user):
        speech_text = 'following me...'
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Dance')
def dance_like_a_monster():
    if(user_name == default_user):
        speech_text = "Self Made is dancing like a monster, do you like it?"
        ser.write('Dance'.encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master, go away'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    face_rec = threading.Thread(target=facerec.detect_user_thread)
    face_rec.start()
    app.run()
