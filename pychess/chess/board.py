import numpy as np


class Board:
    def __init__(self):

        self.board = None
        self.unicode_pieces = ["♟︎", "♞", "♝", "♜", "♛", "♚", "♙", "♘", "♗", "♖", "♕", "♔"]
        self.FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.WHITE = 0
        self.BLACK = 1
        self.UNSIGNED_LONG_1 = np.ulonglong(1)
        self.SQUARE_NAMES = [file + rank for rank in self.RANKS for file in self.FILES]

        self.printable_board = []

    def set_board(self, board):
        self.board = board

    def get_printable_board(self):
        return self.board

    # def print_board(self):

    #     # Used for debugging purposes and a way for the user to see the board
    #     self.set_printable_board()

    #     print("\n")

    #     for rank in range(8):
    #         for file in range(8):
    #             square = rank * 8 + file
    #             if not file:
    #                 print("  " + str(8 - rank) + " ", end="")

    #             print(" " + self.unicode_pieces[self.printable_board[square]] if self.printable_board[square] is not None else " -", end="")

    #         print("")

    #     print("\n     a b c d e f g h\n\n")
