"""
team 3 alexa_w_all_to_one.py

This file links alexa with websocket communication with serial communication

With this file, there can be communications between 3 robots to do various
programmed tasks
"""
#imports
from flask import Flask
from flask_ask import Ask, statement, audio, current_stream
import serial, time
from websocket.robot_chat_client import RobotChatClient

#global vars
app = Flask(__name__)
ask = Ask(app, '/')

ser = serial.Serial('/dev/ttyUSB0', 9600)
print("\nSerial Port open, opening connecting to chat client....\n")
time.sleep(1)

#import Face_recognition.facerec_webcam
speech_unavailable_text = 'Sorry you must sign in first'
signed_in = 1
name = 'Unknown'
username = 'baymax'
ngrok_link = 'ws://35cbc5645e74.ngrok.io'


# functions regarding websocket communications--------------------------------
def test_callback(message_dict):
    
    if message_dict['type'] == 'message':
        print('{0} : {1}'.format(message_dict['user'],message_dict['message']))

    elif message_dict['type'] == 'command':
        print('Global Target: {0} Command: {1}'.format(
              message_dict['user'],
              message_dict['command']))

        if message_dict['user'] == 'all' or message_dict['user'] == username:
            print(message_dict['command'])
            ser.write(message_dict['command'].encode('utf-8'))
            

    elif message_dict['type'] == 'users':
        print('Number of users: {}'.format(message_dict['count']))

def Connected_Chat():
    global client
    client = RobotChatClient(ngrok_link, callback=test_callback)
    time.sleep(1)
    print('Baymax has connected')
    client.send({'type': 'message', 'user': username,
                'message': 'Baymax has connected' })

def chatting():
    string = input()
    while(string != 'quit'):
        client.send({'type': 'message', 'user': username, 'message': string})
        ser.write(string.encode('utf-8'))
        string = input()

    client.send({'type': 'message',
                 'user': 'User Disconnected',
                 'message': 'Baymax'})

    print("please use ctrl + c to end the program")

# Intents regarding alexa ----------------------------------------------------
# Commands that only effect this robot #######################################
@ask.intent('facerec')
def facerec():
    speech_text = 'Sorry I am unable to sign you in. Please make sure you are directly facing the camera.'
    name = facerec_webcam.facecap()
    global signed_in
    print(name)
    if name == "Srikar" :
        speech_text = 'Hello Srikar, you are signed in'
        signed_in = 1
    elif name == "Bailey" :
        speech_text = 'Hello Bailey, you  are signed in'
        signed_in = 1
    elif name == "Steven" :
        speech_text = 'Hello Steven, you are signed in'
        signed_in = 1
    else:
        speech_text = 'Sorry I am unable to sign you in. Please make sure you are directly facing the camera.'
        signed_in = 0
    return statement(speech_text).simple_card('my robot', speech_text)

@ask.intent('wander')
def wander():
    global signed_in
    if(signed_in):
        speech_text = 'Time for a stroll'
        ser.write(b'1')
        return statement(speech_text).simple_card('my robot', speech_text)
    else:
        return statement(speech_unavailable_text).simple_card('my robot', speech_unavailable_text)

@ask.intent('Dance')
def Dance():
    global signed_in
    if(signed_in):
        speech_text = 'Time to Dance!'
        ser.write(b'2')
        
    return statement(speech_text).simple_card('my robot', speech_text)

@ask.intent('halt')
def halt():
    speech_text = 'I will stop moving'
    protocol = "0\n"
    ser.write(b'0')
    return audio(speech_text).stop().simple_card('my robot', speech_text)

@ask.intent('forward')
def Forward():
    
    chat_message = "Moving Forward"
    speech_text = 'FORWARD!'

    ser.write(b'4')

    if chat_message != "":   
        client.send({ 
            'type': 'message', 
            'user': username,
            'message': chat_message})

    return statement(speech_text).simple_card('my robot', speech_text)

@ask.intent('IAmSatisfied')
def satisfied():
    speech = 'Of course!'
    stream_url = 'https://archive.org/download/balalala_202012/balalala.mp3'
    
    ser.write(b'0')
    chat_message = "Has Stopped"

    if chat_message != "":
        client.send({
            'type': 'message',
            'user': username,
            'message': chat_message})

    return audio(speech).play(stream_url)

@ask.intent('Wake')
def stand_up():
    speech = 'Will do!'
    stream_url = 'https://archive.org/download/baymax_greeting/hello-i-am-baymax-your-personal-healthcare-companion.mp3'
    
    ser.write(b'5')
    chat_message = "Is Waking Up!"

    if chat_message != "":
        client.send({
            'type': 'message',
            'user': username,
            'message': chat_message})
    
    return audio(speech).play(stream_url)

# All robot intents##########################################################
@ask.intent('allstop')
def OthersStop():
    command = "0"
    speech_text = 'I asked all robots to stop'

    ser.write(command.encode('utf-8'))

    if command != "":
        client.send({'type': 'command',
                     'user': 'all',
                     'command': command})

    return statement(speech_text).simple_card('my robot', speech_text)

@ask.intent('allforward')
def allForward():
    command = "4"
    speech_text = 'I asked all robots to go forward'

    ser.write(command.encode('utf-8'))

    if command != "":
        client.send({'type': 'command',
                     'user': 'all',
                     'command': command})
    return statement(speech_text).simple_card('my robot', speech_text)

@ask.intent('AllWander')
def allWander():
    command = "1"
    speech_text = 'I asked all robots to wander'

    ser.write(command.encode('utf-8'))

    if command != "":
        client.send({'type': 'command',
                     'user': 'all',
                     'command': command})

    return statement(speech_text).simple_card('my robot', speech_text)

# built in amazon intents ###################################################
@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the stream.').stop()

@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)
