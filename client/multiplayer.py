import wordle
from common import clear, write, detect_keypress
import platform

import socket

PORT = 6741
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

DISCONNECT_MSG = '!disconnect'
HOST_MSG = '!host'
JOIN_MSG = '!join'

class WordleMultiplayer(wordle.Wordle):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = ''
    looping = True

    def run_multiplayer(self):
        clear()

        username = input('Enter your username: ')
        self.client.connect(ADDR)
        self.client.send(username.encode())

        msg = self.client.recv(1024).decode()
        write(msg[4:] + '\n')

        if msg [:3] != '200':
            return -1
        self.username = username

        while self.looping:
            text = """
1. Host a Game
2. Join a Game
3. Exit
>> """
            write(text)
            key = detect_keypress()

            if platform.system() in ['Windows', 'Darwin']:
                key = key[1]

            match key:
                case '1':
                    pass

                case '2':
                    pass

                case '3':
                    pass