from common import clear, write, detect_keypress

import random
import time
from pynput.keyboard import Key
from colorama import Fore, Back, Style
from copy import deepcopy
from os.path import join
from playsound3 import playsound
filename = '5-letter-words.txt'

class Wordle:
    board = []
    bottom_text = ''
    current_word = ''

    word_buffer = [' ', ' ', ' ', ' ', ' ']
    word_buffer_index = 0
    word_buffer_len = 0

    all_words = []
    all_letters = {}

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

        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.all_letters[letter] = 'b'

        self.choose_random_word()

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
                        match board_elem[1]:
                            case 'g':
                                playsound(join('assets', 'green_sound.mp3'), block=False)
                            
                            case 'y':
                                playsound(join('assets', 'yellow_sound.mp3'), block=False)

                            case 'w':
                                playsound(join('assets', 'white_sound.mp3'), block=False)
                        
                        time.sleep(0.300)

                write('\n', flush=False)
            write('')
        
        write(self.bottom_text + '\n\n\n')
        if self.animate_now: self.animate_now = False

    def print_keyboard(self):
        key_layout = 'QWERTYUIOPASDFGHJKLZXCVBNM'

        for key in key_layout:
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
        key = detect_keypress()

        if str(key)[0] == '\'' and self.word_buffer_len < 5:
            self.word_buffer[self.word_buffer_len] = str(key)[1].capitalize()
            self.word_buffer_len += 1
        
        elif key == Key.backspace and self.word_buffer_len > 0:
            self.word_buffer_len -= 1
            self.word_buffer[self.word_buffer_len] = ' '

        elif key == Key.enter:
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

        for elem in temp_buf:
            self.all_letters[elem[0]] = elem[1] if self.all_letters[elem[0]] != 'g' else 'g'

        if color_buf == ['g', 'g', 'g', 'g', 'g']:
            self.has_won = 1

    def run(self):
        clear()
        self.choose_random_word()

        while self.has_won == 0:
            self.print_board()
            self.print_keyboard()
            self.take_input()
        
        self.print_board()
        if self.has_won == 1:
            self.bottom_text = 'YOU SUCCESSFULLY GUESSED THE WORD!!!!!'

        else:
            self.bottom_text = f'The word was {self.current_word.upper()} :c'

        self.print_board()
        time.sleep(3)
            


if __name__ == '__main__':
    clear()
    wordle = Wordle()

    wordle.run()