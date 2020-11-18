from flask import Flask
from flask_ask import Ask, statement
import facerec as facerec
import threading

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('WhoFace')

def who_face():
    speech_text = 'I see {}'.format(facerec.name)
    return statement(speech_text).simple_card('Johnny', speech_text)


if __name__== '__main__':
    face_rec = threading.Thread(target=facerec.facerec_thread)
    face_rec.start()
    app.run()
