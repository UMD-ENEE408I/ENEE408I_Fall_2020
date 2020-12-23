#!/usr/bin/env python3
# Allows Alexa to command the Balboa to stand up or fall down
# Derived from examples in the Flask-Ask repo: https://github.com/johnwheeler/flask-ask

#within simple_card 'Baymax' is associated with the skills name

#imports
import serial, time

from flask import Flask
from flask_ask import Ask, statement


#global vars
app = Flask(__name__)
ask = Ask(app, '/')


#Various alexa commands. These are linked to alexa development services.
@ask.intent('GetHerDone')
def stand_up():
    speech_text = 'Yeeeeeeeeeeeee Haaaw! Getta long little doggy'
    ser.write(b'forward')
    return statement(speech_text).simple_card('Baymax', speech_text)

@ask.intent('IAmSatisfied')
def law_down():
    speech_text = 'See you soon'
    ser.write(b'brake')
    return statement(speech_text).simple_card('Baymax', speech_text)

@ask.intent('Wake')
def stand_up():
    speech_text = 'Hello. I am Baymax, your personal healthcare companion.'
    ser.write(b'forward')
    time.sleep(2)
    ser.write(b'brake')

    return statement(speech_text).simple_card('Baymax', speech_text)

@ask.intent('Dance')
def Dance():
    speech_text = 'I hope you like my tune choice'
    protocol = "2\n"
    ser.write(protocol.encode('utf-8'))
    stream_url = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'
    return audio(speech_text).play(stream_url, offset=0)


#main
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    app.run()
