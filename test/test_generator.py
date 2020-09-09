from random import shuffle, randint
from enum import Enum
from copy import deepcopy


class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

class SudokuGenerator:

    def __init__(self):
        self.difficulty = Difficulty.EASY
        self.new_board()

    def print(self):
        for row in self.board:
            print(row)

    def solve(self, board):
        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        shuffle(num_list)
        for i in num_list:
            # If the number is valid, add it to the board.
            if self.check_row(i, row, board) and self.check_grid(i, row, col, board) and self.check_column(i, col, board):
                board[row][col] = i

                # Try to continue solving the board with the given value that has been added.
                if self.solve(board):
                    return True

                # If the board can't be solved with the selected number, reset it to zero, and try again with a different number.
                board[row][col] = 0

        return False

    def generate(self):
        # Easy sudoku boards will contain 36 clues, medium will contain 31 clues, and hard will contain 22 clues.
        if self.difficulty == Difficulty.EASY:
            counter = 81 - 37
        elif self.difficulty == Difficulty.MEDIUM:
            counter = 81 - 32
        elif self.difficulty == Difficulty.HARD:
            counter = 81 - 23

        while counter >= 0:
            rand_row = randint(0, 8)
            rand_col = randint(0, 8)
            if self.board[rand_row][rand_col] == 0:
                continue

            current_val = self.board[rand_row][rand_col]

            self.board[rand_row][rand_col] = 0

            # When copying a list of lists, a deep copy is required to safely make edits
            # to the nested list without those changes being reflected in the original.
            temp_board = deepcopy(self.board)

            if self.solve(temp_board):
                counter -= 1
            else:
                self.board[rand_row][rand_col] = current_val

    def check_row(self, num, row, board):
        return num not in board[row]

    def check_column(self, num, col, board):
        return num not in (item[col] for item in board)

    def check_grid(self, num, row, col, board):
        grid = []
        if row < 3:
            if col < 3:
                grid = [x[:3] for x in board[:3]]
            elif col >= 3 and col < 6:
                grid = [x[3:6] for x in board[:3]]
            elif col >= 6:
                grid = [x[6:9] for x in board[:3]]
        if row >= 3 and row < 6:
            if col < 3:
                grid = [x[:3] for x in board[3:6]]
            elif col >= 3 and col < 6:
                grid = [x[3:6] for x in board[3:6]]
            elif col >= 6:
                grid = [x[6:9] for x in board[3:6]]
        if row >= 6:
            if col < 3:
                grid = [x[:3] for x in board[6:]]
            elif col >= 3 and col < 6:
                grid = [x[3:6] for x in board[6:]]
            elif col >= 6:
                grid = [x[6:9] for x in board[6:]]
        grid_vals = [item for sublist in grid for item in sublist]

        return num not in grid_vals

    def check_input(self, num, row, col, board):
        if self.check_row(num, row, board) and self.check_grid(num, row, col, board) and self.check_column(num, col, board):
            return True
        else:
            return False

    def find_empty(self, board):
        # For every row on the board
        for i in range(len(board)):
            # For every column in each row
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return i, j

        return None

    def new_board(self):
        self.board = [[0 for col in range(9)] for row in range(9)]
        self.solve(self.board)
        self.generate()


if __name__ == '__main__':
    sud = SudokuGenerator()
    sud.print()
