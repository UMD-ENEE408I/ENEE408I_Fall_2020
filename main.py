import serial
from flask import Flask
from flask_ask import Ask, statement, audio, current_stream
from robot_chat_client import RobotChatClient
import facerec as facerec
import threading

app = Flask(__name__)
ask = Ask(app, '/')

def test_callback(message_dict):
    print('Received dictionary {}'.format(message_dict))
    print('The message is type {}'.format(message_dict['type']))

    if message_dict['type'] == 'message':
        print('Value of field foo: {}'.format(message_dict['foo']))

    if message_dict['type'] == 'users':
        print('Number of users: {}'.format(message_dict['count']))
        
    #if format(message_dict['foo']) == 'Dance':
        #dance()

@ask.intent('Dance')
def dance():
    speech_text = 'Go Maryland!'
    stream_url='https://archive.org/download/victory_20201209_1730/Victory.mp3'
    ser.write(b'd')
    #client.send({'type': 'message','user': 'Matt','foo': 'Dance'})
    return audio(speech_text).play(stream_url)

@ask.intent('WhoFace')
def who_face():
    speech_text = 'I see {}'.format(facerec.name)
    return statement(speech_text).simple_card('HERB', speech_text)

@ask.intent('GoForward')
def go_forward():
    speech_text = 'Forward march'
    ser.write(b'f')
    return statement(speech_text).simple_card('Herb', speech_text)

@ask.intent('GoBackward')
def go_backward():
    speech_text = 'Beep. Beep. Beep.'
    ser.write(b'b')
    return statement(speech_text).simple_card('Herb', speech_text)

@ask.intent('StopAll')
def stop():
    speech_text = 'Ceasing acceleration'
    ser.write(b's')
    return statement(speech_text).simple_card('Herb', speech_text)

@ask.intent('Roam')
def roam():
    speech_text = 'Roaming around at the speed of sound'
    ser.write(b'w')
    return statement(speech_text).simple_card('Herb', speech_text)

if __name__ == '__main__':
    print('Creating RobotChatClient object')
    client = RobotChatClient('ws://localhost:5001', callback=test_callback)
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    face_rec = threading.Thread(target=facerec.show_camera)
    face_rec.start()
    app.run()