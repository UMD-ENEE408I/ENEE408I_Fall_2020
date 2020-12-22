from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio
import serial
import threading
import camera_function as cf
from robot_chat_client import RobotChatClient
import time



app = Flask(__name__)
ask = Ask(app, '/')

group_status = {
    'jack' : 'offline',
    'Andrew' : 'offline',
    'Clovis' : 'offline',
}

user_name = "Unknown"
default_user = "jack"


check_status = None


@ask.launch
def launched():
    speech = "Welcome, Harry Potter is now activating..."
    print("launch...")
    group_status['jack'] = 'online'
    return statement(speech)


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
        if message_dict['target'] == default_user:
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
                    cf.function_index = 2;


    elif message_dict['type'] == 'Response':
        if message_dict['receiver'] == default_user:
            check_status = message_dict['message']


if __name__ == '__main__':
    client_Yuchen = RobotChatClient('ws://d7d1f0f0118d.ngrok.io', callback=test_callback)
    face_rec = threading.Thread(target=cf.run_cam_thread)
    face_rec.start()
    client_Yuchen.send({
             'type': 'new_user',
             'Username': 'jack',
             })
    app.run()