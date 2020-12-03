# this code 

from robot_chat_client import RobotChatClient
import time

USER = 'Yuchen'
# serial communication
ser = serial.Serial('/dev/ttyUSB0', 9600)


def test_callback(message_dict):
    global ser
    print('Received dictionary {}'.format(message_dict))
    print('The message is type {}'.format(message_dict['type']))

    if message_dict['type'] == 'new_user':
        print('Value of field foo: {}'.format(message_dict['Username']))

    elif message_dict['type'] == 'users':
        print('Number of users: {}'.format(message_dict['count']))

    elif message_dict['type'] == 'command':
        if message_dict['target'] == USER
            print('Command target: {}\n'.format(message_dict['target']))
            print("The command is: " + message_dict['command_name'] + '\n')
            ser.write(message_dict['command_name'].encode());

# Run this script directly to invoke this test sequence
if __name__ == '__main__':
    print('Creating RobotChatClient object')
    client = RobotChatClient('ws://localhost:5001', callback=test_callback)



    time.sleep(1)
    print('Joining the server...')

    # report who is joining...
    client.send({'type': 'new_user',
                 'Username': 'Yuchen',
                 })

    # wait for 10 seconds
    time.sleep(10.0)
    client.send({'type': 'command',
                 'target': 'Yuchen',
                 'command_name': 'Self_Driving'})


     # wait for 15 seconds
    time.sleep(15.0)
    client.send({'type': 'command',
                 'target': 'Yuchen',
                 'command_name': 'Stop'})

    print('Waiting for ctrl+c')
