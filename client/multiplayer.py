import wordle
from common import clear, write, detect_keypress, flush_input

import platform
import socket
import time
import threading

PORT = 6741
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

DISCONNECT_MSG = '!disconnect'
HOST_MSG = '!host'
JOIN_MSG = '!join'
ABORT_MSG = '!abort'
START_MSG = '!start'

class WordleMultiplayer(wordle.Wordle):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = ''
    looping = True
    run_message_thread = True
    gamemode = 0
    logged_join_messages = []

    def recv_msg(self):
        while True:
            if self.run_message_thread: break
            msg = self.client.recv(1024).decode()

            if msg.startswith('067'):
                write(msg[4:] + '\n', flush=True)
                self.logged_join_messages.append(msg[4:] + '\n')

    def run_multiplayer(self):
        clear()

        flush_input()
        username = input('Enter your username: ')
        self.client.connect(ADDR)
        self.client.send(username.encode())

        msg = self.client.recv(1024).decode()
        write(msg[4:] + '\n')

        if msg [:3] != '200':
            return -1
        self.username = username

        while self.looping:
            clear()
            text = """
1. Host a Game
2. Join a Game
3. Exit
>> """
            write(text)
            key = str(detect_keypress())

            match key:
                case '1':
                    message_thread = threading.Thread(target=self.recv_msg)
                    clear()
                    text = """
Choose a Gamemode:
1. Gamemode 1
2. Gamemode 2
3. Gamemode 3
>> """
                    write(text, resetcursor=True)
                    key = str(detect_keypress())

                    if not key in ['1', '2', '3']:
                        continue
                    key = int(key)

                    clear()
                    flush_input()
                    password = input('Enter your password: ')

                    clear()
                    self.client.send(f'{HOST_MSG} {password} {self.gamemode}'.encode())
                    msgg = self.client.recv(1024).decode()

                    write(msgg[4:] + '\n')
                    if msgg[:3] != '200':
                        time.sleep(3)
                        continue

                    self.logged_join_messages = []
                    message_thread.start()
                    while True:
                        clear()
                        write(msgg[4:] + '\n', resetcursor=True)
                        write('Press \'W\' to start the match.\n')
                        write('Press \'S\' on your keyboard to abort the room.\n')
                        for logs in self.logged_join_messages:
                            write(logs)
                        write('\n')

                        key = str(detect_keypress())

                        if key == 's':
                            self.run_message_thread = False
                            message_thread.join()

                            self.client.send(ABORT_MSG.encode())
                            message = self.client.recv(1024).decode()

                            write(message[4:])
                            time.sleep(3)
                            break

                        elif key == 'w':
                            self.run_message_thread = False
                            message_thread.join()
                
                # TODO: continue with join msg logic in both server and client
                case '2':
                    message_thread = threading.Thread(target=self.recv_msg)
                    clear()

                    self.client.send(JOIN_MSG.encode())
                    hosted_rooms = self.client.recv(2048).decode()
                    hosted_dict = {} # room_id -> [room_owner, password] 

                    if hosted_rooms.startswith('201'):
                        write(hosted_rooms[4:] + '\n')
                        time.sleep(3)
                        continue

                    hosted_rooms = hosted_rooms.split(';')
                    for room in hosted_rooms:
                        if room == '':
                            continue

                        roomsplit = room.split(sep=',')
                        roomsplit = [x.split(':') for x in roomsplit]
                        hosted_dict[roomsplit[0][1]] = [roomsplit[1][1], roomsplit[2][1]] 

                    for room_id, room_data in hosted_dict.items():
                        write(f'{room_data[0]}\'s room with ID {room_id}.\n')

                    flush_input()
                    room_id = input('Enter the Room ID you wanna join: ')
                    room_pass = input('Enter the password for the room: ')
                    self.client.send(f'{JOIN_MSG} {room_id} {room_pass}'.encode())
                    msgg = self.client.recv(1024).decode()

                    write(msgg[4:] + '\n')
                    if msgg[:3] != '200':
                        time.sleep(3)
                        continue

                    self.logged_join_messages = []
                    message_thread.start()
                    while True:
                        clear()
                        write(msgg[4:] + '\n', resetcursor=True)
                        write('Press \'S\' to leave the room.')
                        for logs in self.logged_join_messages:
                            write(logs)
                        write('\n')

                        key = str(detect_keypress())

                        if key == 's':
                            self.run_message_thread = False
                            message_thread.join()

                            self.client.send(ABORT_MSG.encode())
                            message = self.client.recv(1024).decode()

                            write(message[4:])
                            time.sleep(3)
                            break

                case '3':
                    self.client.send(DISCONNECT_MSG.encode())
                    self.looping = False

if __name__ == '__main__':
    x = WordleMultiplayer()
    x.run_multiplayer()
    flush_input()