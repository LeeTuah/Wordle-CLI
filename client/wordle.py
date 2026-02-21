from common import clear, write, detect_keypress, flush_input

import random
import time
from pynput.keyboard import Key
from colorama import Fore, Back, Style
from copy import deepcopy
import sounddevice as sd
import numpy as np
filename = '5-letter-words.txt'

def play_sound(sound: str):
    freq = 1500 if sound == 'g' else 850 if sound == 'y' else 200
    decay = 8 if sound == 'g' else 10 if sound == 'y' else 12
    sr = 44100
    duration = 0.4
    amp = 0.7 if sound == 'w' else 0.5

    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    s = amp * np.exp(-decay * t) * np.sin(2 * np.pi * freq * t)
    sd.play(s, sr)
    sd.wait()

class Wordle:
    board = []
    bottom_text = ''
    current_word = ''

    word_buffer = [' ', ' ', ' ', ' ', ' ']
    word_buffer_index = 0
    word_buffer_len = 0

    all_words = []
    all_letters = {}
    all_chars = 'QWERTYUIOPASDFGHJKLZXCVBNM'

    animate_now = False
    has_won = 0

    def __init__(self):
        for i in range(5):
            self.board.append([])
            for _ in range(5):
                self.board[i].append([' ', 'w'])

        with open(filename) as file:
            for line in file:
                self.all_words.append(line[0:-1])

        for letter in self.all_chars:
            self.all_letters[letter] = 'b'

        self.choose_random_word()

    # TODO: Add a smoother toggleable animation 
    def print_board(self):
        write('', resetcursor=True)
        for i in range(5):
            using_buffer = (i == self.word_buffer_index)

            for x in range(3):
                for j in range(5):
                    board_elem = self.board[i][j]

                    if i < self.word_buffer_index:
                        write(Fore.BLACK, flush=False)
                        if using_buffer or board_elem[1] == 'w':
                            write(Back.WHITE, flush=False)

                        elif board_elem[1] == 'g':
                            write(Back.GREEN, flush=False)

                        elif board_elem[1] == 'y':
                            write(Back.YELLOW, flush=False)

                    write(
                        '┌───┐' if x == 0 else 
                        ('| ' + (self.word_buffer[j] if using_buffer else board_elem[0]) + ' |' if x == 1 else '└───┘')
                          + Style.RESET_ALL, flush=(x == 1)
                    )
                    if i == self.word_buffer_index - 1 and self.animate_now and x == 1:
                        play_sound(board_elem[1])

                write('\n', flush=False)
            write('')
        
        write(self.bottom_text + '\n\n\n')
        if self.animate_now: self.animate_now = False

    def print_keyboard(self):
        for key in self.all_chars:
            string = ''

            match self.all_letters[key]:
                case 'g':
                    string = Fore.BLACK + Back.GREEN

                case 'y':
                    string = Fore.BLACK + Back.YELLOW

                case 'w':
                    string = Fore.BLACK + Back.WHITE

            write(f'{string} {key} {Style.RESET_ALL}', flush=False)
            
            if key == 'P': write('\n ')
            elif key == 'L': write('\n   ')
            elif key == 'M': write('\n\n')

    def choose_random_word(self):
        self.current_word = random.choice(self.all_words).upper()

    def take_input(self):
        self.bottom_text = ' ' * 100
        key = str(detect_keypress()).upper()

        if str(key) in self.all_chars and self.word_buffer_len < 5:
            self.word_buffer[self.word_buffer_len] = str(key)
            self.word_buffer_len += 1

        elif key == 'BACKSPACE' and self.word_buffer_len > 0:
            self.word_buffer_len -= 1
            self.word_buffer[self.word_buffer_len] = ' '

        elif key == 'ENTER':
            if self.word_buffer_len != 5:
                self.bottom_text = 'Complete the word first!'
                return
            
            if not "".join(self.word_buffer).lower() in self.all_words:
                self.bottom_text = 'This word is not present in the program\'s dictionary.'
                return

            self.match_guess()
            self.board[self.word_buffer_index] = self.word_buffer

            self.word_buffer_index += 1
            self.word_buffer = [' ', ' ', ' ', ' ', ' ']
            self.word_buffer_len = 0

            if self.word_buffer_index >= 5 and self.has_won != 1:
                self.has_won = -1

    def match_guess(self):
        word_buf = []
        color_buf = []

        for (index, letter) in enumerate(self.word_buffer):
            if not letter in self.current_word:
                word_buf.append(letter)
                color_buf.append('w')
                continue
            
            if letter == self.current_word[index]:
                if word_buf.count(letter) < self.current_word.count(letter):
                    color_buf.append('g')
                else:
                    color_buf.append('w')

                word_buf.append(letter)

            else:
                if word_buf.count(letter) < self.current_word.count(letter):
                    color_buf.append('y')
                else:
                    color_buf.append('w')

                word_buf.append(letter)
        
        temp_buf = []
        for x in range(5):
            temp_buf.append([word_buf[x], color_buf[x]])

        self.word_buffer = deepcopy(temp_buf)
        self.animate_now = True

        hierarchy = ['b', 'w', 'y', 'g']
        for elem in temp_buf:
            if hierarchy.index(self.all_letters[elem[0]]) < hierarchy.index(elem[1]):
                self.all_letters[elem[0]] = elem[1] 

        if color_buf == ['g', 'g', 'g', 'g', 'g']:
            self.has_won = 1

    # TODO: Add "Today's Wordle" from NYT
    def run(self):
        clear()
        self.choose_random_word()

        while self.has_won == 0:
            self.print_board()
            self.print_keyboard()
            self.take_input()
        
        self.print_board()
        if self.has_won == 1:
            self.bottom_text = 'YOU GUESSED THE WORD!!!!!'

        else:
            self.bottom_text = f'The word was {self.current_word.upper()} :c'

        self.print_board()
        time.sleep(3)       


if __name__ == '__main__':
    clear()
    wordle = Wordle()

    wordle.run()
    flush_input()