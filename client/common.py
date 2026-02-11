from sys import stdout
import platform
from os import system
from pynput.keyboard import Key, Listener

key_pressed = ''

def detect_keypress():
    def on_press(key):
        global key_pressed
        key_pressed = key
        return False
    
    with Listener(on_press=on_press) as listener: # type: ignore
        listener.join()

    global key_pressed
    return key_pressed

def clear():
    system('cls' if platform.system() == 'Windows' else 'clear')

def reset_cursor():
    stdout.write('\033[H')

def write(message: str, *, flush = True, resetcursor = False):
    if resetcursor: reset_cursor()
    stdout.write(message)
    if flush: stdout.flush()

if __name__ == '__main__':
    while True:
        print(detect_keypress())