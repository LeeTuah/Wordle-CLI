import sys
import platform
import os
from time import sleep

key_pressed = ''

def detect_keypress():
    if platform.system() in ['Windows', 'Darwin']:
        from pynput.keyboard import Listener

        def on_press(key):
            global key_pressed
            key_pressed = key
            return False
        
        with Listener(on_press=on_press) as listener: # type: ignore
            listener.join()

        global key_pressed
        return key_pressed
    
    elif platform.system() == 'Linux':
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
    sys.stdout.write(message + '\n')
    if flush: sys.stdout.flush()

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    
    except:
        import termios, tty
        termios.tcflush(sys.stdin, termios.TCIFLUSH)  # type: ignore