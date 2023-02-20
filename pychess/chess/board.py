import numpy as np


class Board:
    def __init__(self):
        self.unicode_pieces = ["♟︎", "♞", "♝", "♜", "♛", "♚", "♙", "♘", "♗", "♖", "♕", "♔"]
        self.color_to_move = None
        self.white_castle_kingside = False
        self.black_castle_kingside = False
        self.white_castle_queenside = False
        self.black_castle_queenside = False
        self.en_passant_target_square = None

        self.UNSIGNED_LONG_1 = np.ulonglong(1)
        self.WHITE = 0
        self.BLACK = 1
        self.FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.SQUARE_NAMES = [file + rank for rank in self.RANKS for file in self.FILES]

        self.white_pawns = np.uint64(0)
        self.black_pawns = np.uint64(0)
        self.white_knights = np.uint64(0)
        self.black_knights = np.uint64(0)
        self.white_bishops = np.uint64(0)
        self.black_bishops = np.uint64(0)
        self.white_rooks = np.uint64(0)
        self.black_rooks = np.uint64(0)
        self.white_queens = np.uint64(0)
        self.black_queens = np.uint64(0)
        self.white_king = np.uint64(0)
        self.black_king = np.uint64(0)
        self.full_board = np.uint64(0)
        self.printable_board = []

    def parse_fen(self, fen):

        # Example start fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "
        # I split by spaces to make it easier to parse / more readable
        split_fen = fen.split(" ")

        # Parsing the first section of the fen. Finding the piece positions
        # and setting them to their corresponding squares
        piece_positions = split_fen[0].replace("/", "")

        fen_index = 0
        board_index = 0
        while fen_index < len(piece_positions):
            if piece_positions[fen_index].isalpha():
                char = piece_positions[fen_index]
                if char == "P":
                    self.white_pawns = self.set_bit(self.white_pawns, board_index)
                elif char == "R":
                    self.white_rooks = self.set_bit(self.white_rooks, board_index)
                elif char == "B":
                    self.white_bishops = self.set_bit(self.white_bishops, board_index)
                elif char == "N":
                    self.white_knights = self.set_bit(self.white_knights, board_index)
                elif char == "Q":
                    self.white_queens = self.set_bit(self.white_queens, board_index)
                elif char == "K":
                    self.white_king = self.set_bit(self.white_king, board_index)
                elif char == "p":
                    self.black_pawns = self.set_bit(self.black_pawns, board_index)
                elif char == "r":
                    self.black_rooks = self.set_bit(self.black_rooks, board_index)
                elif char == "b":
                    self.black_bishops = self.set_bit(self.black_bishops, board_index)
                elif char == "n":
                    self.black_knights = self.set_bit(self.black_knights, board_index)
                elif char == "q":
                    self.black_queens = self.set_bit(self.black_queens, board_index)
                elif char == "k":
                    self.black_king = self.set_bit(self.black_king, board_index)
            else:
                board_index += int(piece_positions[fen_index]) - 1

            board_index += 1
            fen_index += 1

        self.set_full_board()

        # Setting the side to move from the fen
        self.color_to_move = self.WHITE if split_fen[1] == "w" else self.BLACK

        # Setting castling rights from the fen
        castling_rights = split_fen[2]
        if "K" in castling_rights:
            self.white_castle_kingside = True
        if "Q" in castling_rights:
            self.white_castle_queenside = True
        if "k" in castling_rights:
            self.black_castle_kingside = True
        if "q" in castling_rights:
            self.black_castle_queenside = True

        # Settings enpassant target square
        self.en_passant_target_square = None if "-" in split_fen[3] else split_fen[3]

    def set_printable_board(self):

        # I'm setting the printable board values to the constant
        # self.unicode_pieces = ["♟︎", "♞", "♝", "♜", "♛", "♚", "♙", "♘", "♗", "♖", "♕", "♔"]
        # So white pawns index is 0, black pawns index is 6

        # I know this is inefficient.... definitely need to change this in the future
        # TODO: what's said above ^

        self.printable_board = []

        for square in range(64):
            if self.get_bit(self.white_pawns, square):
                self.printable_board.append(0)
            elif self.get_bit(self.black_pawns, square):
                self.printable_board.append(6)
            elif self.get_bit(self.white_rooks, square):
                self.printable_board.append(3)
            elif self.get_bit(self.black_rooks, square):
                self.printable_board.append(9)
            elif self.get_bit(self.white_bishops, square):
                self.printable_board.append(2)
            elif self.get_bit(self.black_bishops, square):
                self.printable_board.append(8)
            elif self.get_bit(self.white_knights, square):
                self.printable_board.append(1)
            elif self.get_bit(self.black_knights, square):
                self.printable_board.append(7)
            elif self.get_bit(self.white_queens, square):
                self.printable_board.append(4)
            elif self.get_bit(self.black_queens, square):
                self.printable_board.append(10)
            elif self.get_bit(self.white_king, square):
                self.printable_board.append(5)
            elif self.get_bit(self.black_king, square):
                self.printable_board.append(11)
            else:
                self.printable_board.append(None)

    def set_full_board(self):
        self.full_board = self.white_pawns | self.white_knights | self.white_bishops | self.white_queens | self.white_rooks | self.white_king | self.black_pawns | self.black_knights | self.black_bishops | self.black_queens | self.black_rooks | self.black_king

    def set_bit(self, board, index):
        return board | (self.UNSIGNED_LONG_1 << np.ulonglong(index))

    def get_bit(self, board, square):
        return board & (self.UNSIGNED_LONG_1 << np.ulonglong(square))

    def pop_bit(self, board, index):
        return board ^ (self.UNSIGNED_LONG_1 << index) if self.get_bit(board, index) else 0

    def print_bitboard(self, board):

        # Used for debugging purposes

        print("\n")

        for rank in range(8):
            for file in range(8):
                square = rank * 8 + file
                if not file:
                    print("  " + str(8 - rank) + " ", end="")

                print(" " + str(1 if self.get_bit(board, square) else 0), end="")

            print("")

        print("\n     a b c d e f g h\n\n")
        print("     board state: " + str(board) + "\n\n")

    def print_board(self):

        # Used for debugging purposes and a way for the user to see the board
        self.set_printable_board()

        print("\n")

        for rank in range(8):
            for file in range(8):
                square = rank * 8 + file
                if not file:
                    print("  " + str(8 - rank) + " ", end="")

                print(" " + self.unicode_pieces[self.printable_board[square]] if self.printable_board[square] is not None else " -", end="")

            print("")

        print("\n     a b c d e f g h\n\n")
