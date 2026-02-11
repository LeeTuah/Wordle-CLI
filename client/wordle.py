from common import clear, write, detect_keypress

import random
import time
from pynput.keyboard import Key
filename = '5-letter-words.txt'

class Wordle:
    board = []
    bottom_text = ''
    current_word = ''

    word_buffer = [' ', ' ', ' ', ' ', ' ']
    word_buffer_index = 0
    word_buffer_len = 0

    all_words = []

    def __init__(self):
        
        for i in range(5):
            self.board.append([])
            for _ in range(5):
                self.board[i].append(' ')

        with open(filename) as file:
            for line in file:
                self.all_words.append(line[0:-1])

        self.choose_random_word()

    def print_board(self):
        write('', resetcursor=True)
        for i in range(5):
            write(('┌───┐' * 5) + '\n', flush=False)

            for j in range(5):
                write('| ' + (self.word_buffer[j] if i == self.word_buffer_index else self.board[i][j]) + ' |', flush=False)

            write('\n' + ('└───┘' * 5) + '\n', flush=False)
        
        write(self.bottom_text + '\n')

    def choose_random_word(self):
        self.current_word = random.choice(self.all_words)

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

            self.board[self.word_buffer_index] = self.word_buffer

            self.word_buffer_index += 1
            self.word_buffer = [' ', ' ', ' ', ' ', ' ']
            self.word_buffer_len = 0


if __name__ == '__main__':
    clear()
    wordle = Wordle()

    # print(wordle.board)
    # wordle.print_board()
    # while True:
    #     wordle.choose_random_word()
    #     print(wordle.current_word)
    #     time.sleep(1)

    while wordle.word_buffer_index < 5:
        wordle.print_board()
        wordle.take_input()
