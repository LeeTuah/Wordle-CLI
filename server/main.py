from common import clear, write, detect_keypress

import socket
import threading
import platform
import os
from pynput.keyboard import Key

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 6741
ADDR = (SERVER, PORT)

DISCONNECT_MSG = '!disconnect'
HOST_MSG = '!host'
JOIN_MSG = '!join'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

user_list = {} # username -> {client: socket, addr: address, ingame: bool, room_id: int, room_owner: bool}

def handle_keypress():
    while True:
        key = detect_keypress()

        if (platform.system() in ['Windows', 'Darwin'] and key == Key.backspace) or (platform.system() == 'Linux' and key == 'BACKSPACE'):
            os._exit(0)

def handle_connections(client: socket.socket, addr: socket._RetAddress):
    connected = True
    get_username = True
    valid_username = False
    username = ''

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

        except ConnectionResetError, ConnectionAbortedError, ConnectionError:
            connected = False

    if valid_username:
        write(f'[LEAVE] {username} has left.')

    else:
        write(f'[LEAVE] ({addr[0]}:{addr[1]}) has left.')

    client.close()

def main():
    clear()
    write('', resetcursor=True)

    server.listen()
    write('[DEBUG] The server is currently listening.....')
    write('[DEBUG] Press \'BACKSPACE\' to shutdown the server.')

    keypress_thread = threading.Thread(target=handle_keypress)
    keypress_thread.start()

    while True:
        client, addr = server.accept()
        write(f'[JOIN] ({addr[0]}:{addr[1]}) has connected.')

        handle_thread = threading.Thread(target=handle_connections, args=(client, addr))
        handle_thread.start()

if __name__ == '__main__':
    main()