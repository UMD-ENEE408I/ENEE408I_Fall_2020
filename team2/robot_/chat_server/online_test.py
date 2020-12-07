from robot_chat_client import RobotChatClient
import serial
from flask import Flask
from flask_ask import Ask, statement


ser = serial.Serial('/dev/ttyUSB0', 9600)
app = Flask(__name__)
ask = Ask(app, '/')

user_name = "Unknown"
default_user = "Yuchen"

check_status = None

@ask.intent("OnlineFriend",default = {'name': ''})
def check_friend(name):
    global check_status
    check_status = None

    target = name;
    client_Yuchen.send({'sender': 'Yuchen'
                 'type': 'command',
                 'target': name,
                 'command_name': 'is_online'});
    while check_status is None: 
        time.sleep(.02)

    if check_status == 'Yes':
        speech_text = '{} is online, wanna have some funs...'.format(name)
    else:
        speech_text = '{} is not online, try to find someone else'.format(name)

    return


def test_callback(message_dict):
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
                if(user_name == default_user):
                    message = 'Yes'
                else:
                    message = 'No'

            client_Yuchen.send({
                'type': 'Response'
                'sender': default_user
                'message': message
                'receiver': message_dict['sender']
                })

    elif message_dict['type'] == 'Response'
        if message_dict['receiver'] == default_user:
            check_status = message_dict['message']


if __name__ == '__main__':
    client_Yuchen = RobotChatClient('ws://7cfccfba9583.ngrok.io', callback=test_callback)