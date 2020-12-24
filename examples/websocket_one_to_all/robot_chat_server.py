#!/usr/bin/env python3
# Below is based heavily on the examples in:
# https://websockets.readthedocs.io/en/stable/intro.html

#python3 robot_chat_server 2> /dev/null

import asyncio
import json
import websockets

USERS = set()

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps({"type": "users", "count": len(USERS)})
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    print('REGISTER')
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    print('UNREGISTER')
    USERS.remove(websocket)
    await notify_users()

async def one_to_all(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            # Hack due to infamiliarity with asyncio
            # List of sockets that are not this socket
            to_notify = [user for user in USERS if user != websocket]
            # If there is anyone to notify, notify all
            if to_notify:
                await asyncio.wait([user.send(message) for user in to_notify])
    except:
        pass
    finally:
        await unregister(websocket)


start_server = websockets.serve(one_to_all, '0.0.0.0', 5001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
