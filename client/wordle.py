class Wordle:
    board = []

    def __init__(self):
        for i in range(5):
            for j in range(5):
                self.board[i][j] = ' '