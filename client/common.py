import sys
import platform
import os
from time import sleep

key_pressed = ''

def detect_keypress():
    if platform.system() == 'Windows':
        import msvcrt
        key = msvcrt.getch()

        if key == b'\r':
            return 'ENTER'
        
        if key == b'\x03': 
            return 'ctrl+c'

        elif key == b'\x08':
            return 'BACKSPACE'

        if key in (b'\x00', b'\xe0'):
            return key + msvcrt.getch()

        return key.decode('utf-8', errors='ignore')

    elif platform.system() in ['Darwin', 'Linux']:
        import tty, termios
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd) # type: ignore
        try:
            tty.setraw(sys.stdin.fileno()) # type: ignore
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # type: ignore
        
        if ch == '\r' or ch == '\n':
            return 'ENTER'
        elif ch == '\x7f' or ch == '\b':
            return 'BACKSPACE'
        elif ch == '\x03':
            sys.exit()
        else:
            return ch.upper()

    return ''

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def write(message: str, *, flush = True, resetcursor = False):
    if resetcursor: sys.stdout.write('\033[H')
    sys.stdout.write(message)
    if flush: sys.stdout.flush()

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

if __name__ == '__main__':
    while True:
        print(detect_keypress())