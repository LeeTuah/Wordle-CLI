from common import clear, write, detect_keypress, flush_input

import socket
import threading
import platform
import os
from pynput.keyboard import Key
import random

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 6741
ADDR = (SERVER, PORT)

DISCONNECT_MSG = '!disconnect'
HOST_MSG = '!host'
JOIN_MSG = '!join'
ABORT_MSG = '!abort'
START_MSG = '!start'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

user_list = {} # username -> {client: socket, addr: address, ingame: bool, room_id: int, room_owner: bool}
hosted_rooms = {} # room_id -> {room_owner: [socket, name], password: str, other_people: [client], gamemode: int}

def handle_keypress():
    while True:
        key = str(detect_keypress())

        if key == '~':
            flush_input()
            os._exit(0)

def send_to_all(message: str, room_id: int, ignore_client: None | socket.socket = None):
    room_data = hosted_rooms[room_id]

    if room_data['room_owner'][0] != ignore_client:
        room_data['room_owner'][0].send(message.encode())

    for person in room_data['other_people']:
        if person == ignore_client:
            continue

        person.send(message.encode())

    print('Sent to everyone <-------------------------------')

def handle_connections(client: socket.socket, addr: socket._RetAddress):
    connected = True
    get_username = True
    valid_username = False
    username = ''
    room_id = 0

    while connected:
        try:
            message = client.recv(1024).decode()

            if not message:
                break

            elif get_username:
                get_username = False
                username = message

                if username in user_list.keys():
                    client.send('403|This username is already logged in, choose a different name.'.encode())
                    connected = False
                    valid_username = False
                    break

                user_list[username] = {'client': client, 'addr': addr, 'ingame': False, 'room_id': 0, 'room_owner': False}
                valid_username = True
                write(f'{username} has connected.')
                client.send('200|You have connected to the server.'.encode())

            elif message.lower().startswith(DISCONNECT_MSG):
                connected = False
                break

            elif message.lower().startswith(ABORT_MSG): # FIXME: When a room owner aborts the room with other people
                owned_room = user_list[username]['room_owner']
                if room_id == 0:
                    client.send('403|You do not have a room hosted to abort.'.encode())
                    continue

                # send_to_all(f'067|{username} has left the room.', room_id, client) # FIXME: Send_to_all not working
                if owned_room:
                    hosted_rooms.pop(room_id)
                else:
                    hosted_rooms[room_id]['other_people'].remove(client)

                user_list[username]['room_owner'] = False

                client.send(f'200|You aborted your room with ID {room_id}.'.encode())
                print(f'Aborted an old room with ID {room_id} for {username}.' if owned_room else f'{username} left the room with ID {room_id}')
                room_id = 0
                user_list[username]['room_id'] = 0

            elif message.lower().startswith(HOST_MSG):
                msgs = message.split(sep=' ')

                if user_list[username]['room_id'] != 0:
                    client.send('403|You already have a room hosted, please delete that room.'.encode())
                    continue

                if len(msgs) != 3:
                    client.send(f'403|Invalid message format, please try again'.encode())
                    continue

                password = msgs[1]
                game_mode = msgs[2]

                room_id = random.randint(11111111, 99999999)
                user_list[username]['room_id'] = room_id
                user_list[username]['room_owner'] = True
                hosted_rooms[room_id] = {'room_owner': [client, username], 'password': password, 'other_people': [], 'gamemode': int(game_mode)}

                client.send(f'200|Your Room ID is {room_id}.'.encode())
                print(f'Created a new room with ID {room_id} for {username}.')

            elif message.lower().startswith(JOIN_MSG):
                msgs = message.split(sep=' ')

                if len(msgs) > 3 or len(msgs) == 2:
                    client.send(f'403|Invalid message format, please try again.'.encode())
                    continue

                if len(msgs) == 1:
                    hosted_rooms_copy = ''
                    for key, value in hosted_rooms.items():
                        hosted_rooms_copy += f"room_id:{key},room_owner:{value['room_owner'][1]},password:{value['password']};"

                    client.send('201|No rooms are hosted right now.'.encode() if hosted_rooms_copy == '' else hosted_rooms_copy.encode())

                if len(msgs) == 3:
                    input_room_id = 0
                    room_pass = msgs[2]
                    try:
                        input_room_id = int(msgs[1])

                    except ValueError:
                        client.send(f'403|Invalid Room ID provided, please try again.'.encode())
                        continue

                    if not input_room_id in hosted_rooms:
                        client.send(f'403|Invalid Room ID provided, please try again.'.encode())
                        continue
                
                    if room_pass != hosted_rooms[input_room_id]['password']:
                        client.send(f'403|Incorrect password for room provided, try again.'.encode())
                        continue

                    room_id = input_room_id
                    hosted_rooms[room_id]['other_people'].append(client)
                    # send_to_all(f'067|{username} has joined the room.', room_id, client) # FIXME: Send_to_all not working
                    client.send(f'200|Successfully joined the room with ID {room_id}'.encode())
                    user_list[username]['room_id'] = room_id
                    print(f'{username} joined in {room_id}.')

            elif message.lower().startswith(START_MSG):
                pass

        except ConnectionResetError, ConnectionAbortedError, ConnectionError:
            connected = False

    # TODO: Destroy the room or remove from room when the player leaves
    if valid_username:
        write(f'[LEAVE] {username} has left.')
        user_list.pop(username)

    else:
        write(f'[LEAVE] ({addr[0]}:{addr[1]}) has left.')

    client.close()

def main():
    clear()
    write('', resetcursor=True)

    server.listen()
    write('[DEBUG] The server is currently listening.....')
    write('[DEBUG] Press \'~\' to shutdown the server.')

    keypress_thread = threading.Thread(target=handle_keypress)
    keypress_thread.start()

    while True:
        client, addr = server.accept()
        write(f'[JOIN] ({addr[0]}:{addr[1]}) has connected.')

        handle_thread = threading.Thread(target=handle_connections, args=(client, addr))
        handle_thread.start()

if __name__ == '__main__':
    main()