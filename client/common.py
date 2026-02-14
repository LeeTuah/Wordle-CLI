import sys
import platform
import os
from pynput.keyboard import Listener
from time import sleep

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
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def reset_cursor():
    sys.stdout.write('\033[H')

def write(message: str, *, flush = True, resetcursor = False):
    if resetcursor: reset_cursor()
    sys.stdout.write(message)
    if flush: sys.stdout.flush()

if __name__ == '__main__':
    while True:
        print(detect_keypress())

def slow_print(msg: str, delay: int = 50):
    for i in msg:
        print(i, flush=True)
        sleep(delay / 1000)

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    
    except:
        import termios, tty
        termios.tcflush(sys.stdin, termios.TCIFLUSH)  # type: ignore