import serial
from flask import Flask
from flask_ask import Ask, statement
import threading
import camera_function as cf
from robot_chat_client import RobotChatClient
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)
app = Flask(__name__)
ask = Ask(app, '/')

user_name = "Unknown"
default_user = "jack"
check_status = None
group_status = {
    'jack' : 'offline',
    'Andrew' : 'offline',
    'Clovis' : 'offline',
}

@ask.launch
def launched():
    speech = "Welcome, Harry Potter is now activating..."
    print("launch...")
    group_status['jack'] = 'online'
    return statement(speech)


@ask.intent('Stop')
def stop():
    speech_text = 'harry potter has stopped. I am dead'
    ser.write('Stop'.encode())
    print(ser.readline())
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Self_Driving_MODE')
def self_Driving():
    if(user_name == default_user):  
        speech_text = 'harry potter enters self driving mode, I am feeling more energized than ever'
        ser.write('Self_Driving'.encode())
        print(ser.readline())
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Face_rec')
def face_rec():
    global user_name 
    user_name = cf.name
    if user_name == default_user:
        speech_text = 'You are {}, welcome!'.format(user_name)
    else:
        speech_text = 'You are {}, emmmmmmm!'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Lock')
def lock_robot():
    global user_name
    user_name = "Unknown"
    speech_text = 'harry potter has locked itself'
    return statement(speech_text).simple_card('Muscles', speech_text)


@ask.intent('forward_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def move_forward(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'harry potter moves foward for {} seconds, do you like turtles?'.format(time);
        ser.write('1 Forward {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('backward_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def backward_duration(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'harry potter moves backward for {} seconds, do you like turtles?'.format(time);
        ser.write('1 Backward {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('left_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def left_duration(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'harry potter turns left for {} secondsm do you like turtles?'.format(time);
        ser.write('1 Left {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)


@ask.intent('right_duration', convert = {'duration': int , 'decimal': int}, default = {'duration': '1', 'decimal': '0'})
def right_duration(duration, decimal):
    if(user_name == default_user):
        divisor = 10
        while(int(decimal) > divisor):
            divisor *= 10
        time = float(duration)+ float(decimal)/float(divisor)
        speech_text = 'harry potter turns right for {} seconds, do you like turtles?'.format(time);
        ser.write('1 Right {}'.format(duration).encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('follow_me')
def april_tag_follow():
    if(user_name == default_user):
        speech_text = 'following me...'
        cf.function_index = 2;
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Stopfollow')
def stop_april_tag_follow():
    if(user_name == default_user):
        speech_text = 'stop following...'
        cf.function_index = 1;
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)

@ask.intent('Dance', default = {'key':''})
def dance_like_a_monster(key):
    catch_phase = ['together','with me', 'all togther']
    if(user_name == default_user):
        if key in catch_phase:
            client_Yuchen.send({'sender': 'jack',
                 'type': 'command',
                 'target': 'all',
                 'command_name': 'Dance'});
            speech_text = "harry potter is dancing with friends, emmmmmmmmm"
        else:
            speech_text = "harry potter is dancing like a monster, do you like it?"

        ser.write('Dance'.encode())
        print(ser.readline().decode())
    else:
        speech_text = 'You are {}, you are not my master'.format(user_name)
    return statement(speech_text).simple_card('Muscles', speech_text)



@ask.intent("OnlineFriend",default = {'name': 'jack'})
def check_friend(name):
    global check_status
    check_status = None
    print(name);
    target = name;
    client_Yuchen.send({'sender': 'jack',
                 'type': 'command',
                 'target': name,
                 'command_name': 'is_online'});
    while check_status is None: 
        time.sleep(.02)

    if check_status == 'Yes':
        group_status[name] = 'online'
        speech_text = '{} is online, wanna have some funs...'.format(name)
    else:
        group_status[name] = 'offline'
        speech_text = '{} is not online, try to find someone else'.format(name)

    print(speech_text)
    return statement(speech_text).simple_card('Muscles', speech_text)



@ask.intent('target_follow', default = {'name': 'jack'})
def target_follow(name):
    print(name)
    if(group_status[name] == 'offline'):
        speech = '{} is currently offline, try later...'.format(name)
    else:
        client_Yuchen.send({
                 'sender': 'jack',
                 'type': 'command',
                 'target': name,
                 'command_name': 'follow'
            })
        speech = '{}.robot will follow him until someone tells to stop...'.format(name)
    print(speech)
    return statement(speech)


def test_callback(message_dict):
    global check_status
    print('Received dictionary {}'.format(message_dict))
    print('The message is type {}'.format(message_dict['type']))

    if message_dict['type'] == 'new_user':
        print('The new user is: {}'.format(message_dict['Username']))

    elif message_dict['type'] == 'users':
        print('Number of users: {}'.format(message_dict['count']))

    elif message_dict['type'] == 'command':
        if message_dict['target'] == default_user or message_dict['target'] == 'all':
            print('Command target: {}\n'.format(message_dict['target']))
            print("The command is: " + message_dict['command_name'] + '\n')

            if message_dict['command_name'] == 'is_online':
                if(group_status[default_user] == 'online'):
                    message = 'Yes'
                else:
                    message = 'No'

                client_Yuchen.send({
                        'type': 'Response',
                        'sender': default_user,
                        'message': message,
                        'receiver': message_dict['sender']
                        })

            elif message_dict['command_name'] == 'follow':
                print("{}'s robot is following him...".format(message_dict['target']))
                cf.function_index = 2

            elif message_dict['command_name'] == 'Dance':
                ser.write("Dance".encode())


    elif message_dict['type'] == 'Response':
        if message_dict['receiver'] == default_user:
            check_status = message_dict['message']


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)



if __name__ == '__main__':
    client_Yuchen = RobotChatClient('ws://864e487b8730.ngrok.io', callback=test_callback)

    face_rec = threading.Thread(target=cf.run_cam_thread)
    face_rec.start()
    app.run()
