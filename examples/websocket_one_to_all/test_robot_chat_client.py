from robot_chat_client import RobotChatClient
import time

usrname = 'Baymax'

def test_callback(message_dict):
    
    if message_dict['type'] == 'message':
        print('{0} : {1}'.format(message_dict['user'],message_dict['foo']))

    if message_dict['type'] == 'users':
        print('Number of users: {}'.format(message_dict['count']))

# Run this script directly to invoke this test sequence
if __name__ == '__main__':
    print('Creating RobotChatClient object')
    client = RobotChatClient('ws://localhost:5001', callback=test_callback)

    time.sleep(1)

    print('User Joined: Baymax Has Connected')
    client.send({'type': 'message',
                 'user': 'User Joined',
                 'foo': 'Baymax'})

    string = input()
    while(string != 'quit'):
        client.send({'type': 'message', 'user': usrname, 'foo': string})
        string = input()

    client.send({'type': 'message',
                 'user': 'User Disconnected',
                 'foo': 'Baymax'})

    print("please use ctrl + c to end the program")

    
