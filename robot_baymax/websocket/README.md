# Robot Chat Example

A simple method to send messages from one to all using a central server. Built using websockets and json serialization.

Install websockets with `pip3 install websockets`.

Usage is simple:
```python
from robot_chat_client import RobotChatClient
import time

def receive_callback(message_dict):
    print('Received {}'.format(message_dict))

if __name__ == '__main__':
    # Replace url with the server's URL
    client = RobotChatClient('ws://localhost:5001', callback=receive_callback)

    time.sleep(1)
    client.send({'type': 'test_message_type',
                 'foo': [1, 2, 3, 4, 5]})
```

## Demonstration on a single computer
Launch the server in a terminal.

`python3 robot_chat_server.py`

Leave the script running in the first terminal. In a second terminal run the below command.

`python3 test_robot_chat_client.py`.

The following will happen:
* The script will connect to the server.
* Receive a message from the server with the number of connected users
* 1 second later, send a message to the server
* Since there is only one connected user, nothing more will happen

Leave the script running in the second terminal. In a third terminal run the below command.

`python3 test_robot_chat_client.py`.

 The following will happen:
 * The script will connect to the server
 * The server will message both connected users with the number of connected users
 * 1 second later, the latest script will send a message to the server
 * The server will forward the message to the other connected client.

Press ctrl+c to close the second client (in the third terminal). The following will happen:
* The server will print an error because the connection was closed without cleaning up (you can ignore this or maybe fix the client if you are interested)
* The remaining client will receive a message from the server with the number of connected users (one)

## Usage
Run the server on a robot.
Run ngrok on the robot running the server. The default port is 5001, so launch ngrok with `ngrok http 5001`.

The client running on the robot with the server can use `ws://localhost:5001` to connect.

The clients on other robots can use `ws://ngrokurl.ngrok.io` to connect to the server (drop the port number).

If everything is setup right, messages sent from one robot will be received by all the other robots.

## AWS
Alternatively you can setup a free server in the AWS cloud to run the server. Then you would use `ws://serveripaddress:5001` in all the clients and ngrok would not be needed.

In this scenario, all messages would first be sent to the server running in the AWS cloud. The server relays all the messages back to all connected clients. This avoids local network access restrictions in the same manner ngrok does.

