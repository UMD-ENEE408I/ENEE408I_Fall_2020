from robot_chat_client import RobotChatClient
import time

def test_callback(message_dict):
    print('Received dictionary {}'.format(message_dict))
    print('The message is type {}'.format(message_dict['type']))

    if message_dict['type'] == 'test_message_type':
        print('Value of field foo: {}'.format(message_dict['foo']))

    if message_dict['type'] == 'users':
        print('Number of users: {}'.format(message_dict['count']))

# Run this script directly to invoke this test sequence
if __name__ == '__main__':
    print('Creating RobotChatClient object')
    client = RobotChatClient('ws://localhost:5001', callback=test_callback)

    time.sleep(1)
    print('Sending a test message')
    client.send({'type': 'test_message_type',
                 'foo': [1, 2, 3, 4, 5]})

    print('Waiting for ctrl+c')
