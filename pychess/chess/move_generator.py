import numpy as np
import math


class MoveGenerator:
    def __init__(self, board):
        self.board = board
        self.knight_attack_squares = []
        self.rook_attack_squares = []
        self.king_attack_squares = []
        self.bishop_attack_squares = []
        self.pawn_attack_squares = [[], []]
        self.WHITE = 0
        self.BLACK = 1
        self.UNSIGNED_LONG_1 = np.ulonglong(1)
        self.color_to_move = 0
        self.not_ab_file = np.ulonglong(18229723555195321596)
        self.not_hg_file = np.ulonglong(4557430888798830399)
        self.not_h_file = np.ulonglong(9187201950435737471)
        self.not_a_file = np.ulonglong(18374403900871474942)

        self.init_attack_squares()

    def calculate_moves(self, color_to_move):
        pass

    def init_attack_squares(self):
        self.populate_knight_attack_squares()
        self.populate_pawn_attack_squares()
        self.populate_king_attack_squares()
        self.populate_bishop_attack_squares()
        self.populate_rook_attack_squares()

        self.print_bitboard(self.bishop_attack_squares[45])
        self.print_bitboard(np.uint64(580964626808963072))

    def populate_rook_attack_squares(self):

        for square in range(64):

            attack_squares = np.uint64(0)

            current_rank = math.floor(square / 8)
            current_file = square % 8

            desired_rank = current_rank + 1
            for _ in range(8):
                if desired_rank > 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + current_file)))
                desired_rank += 1

            desired_rank = current_rank - 1
            for _ in range(8):
                if desired_rank < 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + current_file)))
                desired_rank -= 1

            desired_file = current_file + 1
            for _ in range(8):
                if desired_file > 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(current_rank * 8 + desired_file)))
                desired_file += 1

            desired_file = current_file - 1
            for _ in range(8):
                if desired_file < 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(current_rank * 8 + desired_file)))
                desired_file -= 1

            self.rook_attack_squares.append(attack_squares)

    def populate_bishop_attack_squares(self):

        for square in range(64):

            attack_squares = np.uint64(0)

            current_rank = math.floor(square / 8)
            current_file = square % 8

            desired_rank = current_rank + 1
            desired_file = current_file + 1
            for _ in range(8):
                if desired_rank > 7 or desired_file > 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank += 1
                desired_file += 1

            desired_rank = current_rank + 1
            desired_file = current_file - 1
            for _ in range(8):
                if desired_rank > 7 or desired_file < 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank += 1
                desired_file -= 1

            desired_rank = current_rank - 1
            desired_file = current_file + 1
            for _ in range(8):
                if desired_rank < 0 or desired_file > 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank -= 1
                desired_file += 1

            desired_rank = current_rank - 1
            desired_file = current_file - 1
            for _ in range(8):
                if desired_rank < 0 or desired_file < 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank -= 1
                desired_file -= 1

            self.bishop_attack_squares.append(attack_squares)

    def populate_king_attack_squares(self):

        for square in range(64):

            attack_squares = np.uint64(0)
            board = np.uint64(0)
            board = self.set_bit(board, square)

            if (board >> np.uint64(8)):
                attack_squares = attack_squares | (board >> np.uint64(8))
            if (board << np.uint64(8)):
                attack_squares = attack_squares | (board << np.uint64(8))
            if ((board >> np.uint64(1)) & self.not_h_file):
                attack_squares = attack_squares | (board >> np.uint64(1))
            if ((board >> np.uint64(9)) & self.not_h_file):
                attack_squares = attack_squares | (board >> np.uint64(9))
            if ((board >> np.uint64(7)) & self.not_a_file):
                attack_squares = attack_squares | (board >> np.uint64(7))
            if ((board << np.uint64(1)) & self.not_a_file):
                attack_squares = attack_squares | (board << np.uint64(1))
            if ((board << np.uint64(9)) & self.not_a_file):
                attack_squares = attack_squares | (board << np.uint64(9))
            if ((board << np.uint64(7)) & self.not_h_file):
                attack_squares = attack_squares | (board << np.uint64(7))

            self.king_attack_squares.append(attack_squares)

    def populate_pawn_attack_squares(self):

        for square in range(64):

            attack_squares = np.uint64(0)
            board = np.uint64(0)
            board = self.set_bit(board, square)

            # This is for white pawns
            if ((board >> np.uint64(7)) & self.not_a_file):
                attack_squares = attack_squares | (board >> np.uint64(7))
            if ((board >> np.uint64(9)) & self.not_h_file):
                attack_squares = attack_squares | (board >> np.uint64(9))

            self.pawn_attack_squares[self.WHITE].append(attack_squares)

            # This is for black pawns
            attack_squares = np.uint64(0)

            if ((board << np.uint64(7)) & self.not_h_file):
                attack_squares = attack_squares | (board << np.uint64(7))
            if ((board << np.uint64(9)) & self.not_a_file):
                attack_squares = attack_squares | (board << np.uint64(9))

            self.pawn_attack_squares[self.BLACK].append(attack_squares)

    def populate_knight_attack_squares(self):

        for square in range(64):

            board = np.uint64(0)
            attack_squares = np.uint64(0)
            board = self.set_bit(board, square)

            if ((board >> np.uint64(17)) & self.not_h_file):
                attack_squares = attack_squares | (board >> np.uint64(17))
            if ((board >> np.uint64(15)) & self.not_a_file):
                attack_squares = attack_squares | (board >> np.uint64(15))
            if ((board >> np.uint64(10)) & self.not_hg_file):
                attack_squares = attack_squares | (board >> np.uint64(10))
            if ((board >> np.uint64(6)) & self.not_ab_file):
                attack_squares = attack_squares | (board >> np.uint64(6))
            if ((board << np.uint64(17)) & self.not_a_file):
                attack_squares = attack_squares | (board << np.uint64(17))
            if ((board << np.uint64(15)) & self.not_h_file):
                attack_squares = attack_squares | (board << np.uint64(15))
            if ((board << np.uint64(10)) & self.not_ab_file):
                attack_squares = attack_squares | (board << np.uint64(10))
            if ((board << np.uint64(6)) & self.not_hg_file):
                attack_squares = attack_squares | (board << np.uint64(6))

            self.knight_attack_squares.append(attack_squares)

    def set_bit(self, board, index):
        return board | (self.UNSIGNED_LONG_1 << np.ulonglong(index))

    def get_bit(self, board, square):
        return board & (self.UNSIGNED_LONG_1 << np.ulonglong(square))

    def pop_bit(self, board, index):
        return board ^ (self.UNSIGNED_LONG_1 << index) if self.get_bit(board, index) else 0

    def print_bitboard(self, board):

        # Used for debugging purposes

        print("\n")

        for desired_rank in range(8):
            for desired_file in range(8):
                square = desired_rank * 8 + desired_file
                if not desired_file:
                    print("  " + str(8 - desired_rank) + " ", end="")

                print(" " + str(1 if self.get_bit(board, square) else 0), end="")

            print("")

        print("\n     a b c d e f g h\n\n")
        print("     board state: " + str(board) + "\n\n")
