from flask import Flask
from flask_ask import Ask, statement
import facerec_from_webcam_faster as facerec

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('WhoFace')

def who_face():
    name = facerec.get_name()
    speech_text = 'You are {}'.format(name)
    return statement(speech_text).simple_card('Johnny', speech_text)


if __name__=='__main':
    app.run()

