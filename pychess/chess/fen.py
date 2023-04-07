import numpy as np
from piece import Piece


class Fen():
    def __init__(self):
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
        self.white_board = np.uint64(0)
        self.black_board = np.uint64(0)
        self.piece_board = []
        self.color_to_move = None
        self.white_castle_kingside = False
        self.black_castle_kingside = False
        self.white_castle_queenside = False
        self.black_castle_queenside = False
        self.en_passant_target_square = None
        self.WHITE = 0
        self.BLACK = 1
        self.UNSIGNED_LONG_1 = np.ulonglong(1)

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
                    self.piece_board.append(Piece.WHITE_PAWN)
                elif char == "R":
                    self.white_rooks = self.set_bit(self.white_rooks, board_index)
                    self.piece_board.append(Piece.WHITE_ROOK)
                elif char == "B":
                    self.white_bishops = self.set_bit(self.white_bishops, board_index)
                    self.piece_board.append(Piece.WHITE_BISHOP)
                elif char == "N":
                    self.white_knights = self.set_bit(self.white_knights, board_index)
                    self.piece_board.append(Piece.WHITE_KNIGHT)
                elif char == "Q":
                    self.white_queens = self.set_bit(self.white_queens, board_index)
                    self.piece_board.append(Piece.WHITE_QUEEN)
                elif char == "K":
                    self.white_king = self.set_bit(self.white_king, board_index)
                    self.piece_board.append(Piece.WHITE_KING)
                elif char == "p":
                    self.black_pawns = self.set_bit(self.black_pawns, board_index)
                    self.piece_board.append(Piece.BLACK_PAWN)
                elif char == "r":
                    self.black_rooks = self.set_bit(self.black_rooks, board_index)
                    self.piece_board.append(Piece.BLACK_ROOK)
                elif char == "b":
                    self.black_bishops = self.set_bit(self.black_bishops, board_index)
                    self.piece_board.append(Piece.BLACK_BISHOP)
                elif char == "n":
                    self.black_knights = self.set_bit(self.black_knights, board_index)
                    self.piece_board.append(Piece.BLACK_KNIGHT)
                elif char == "q":
                    self.black_queens = self.set_bit(self.black_queens, board_index)
                    self.piece_board.append(Piece.BLACK_QUEEN)
                elif char == "k":
                    self.black_king = self.set_bit(self.black_king, board_index)
                    self.piece_board.append(Piece.BLACK_KING)
            else:
                board_index += int(piece_positions[fen_index]) - 1
                for x in range(int(piece_positions[fen_index])):
                    self.piece_board.append(None)

            board_index += 1
            fen_index += 1

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

        self.set_full_board()
        self.set_white_board()
        self.set_black_board()

    def set_bit(self, board, index):
        return board | (self.UNSIGNED_LONG_1 << np.ulonglong(index))

    def set_full_board(self):
        self.full_board = self.white_pawns | self.white_knights | self.white_bishops | self.white_queens | self.white_rooks | self.white_king | self.black_pawns | self.black_knights | self.black_bishops | self.black_queens | self.black_rooks | self.black_king

    def set_white_board(self):
        self.white_board = self.white_pawns | self.white_knights | self.white_bishops | self.white_queens | self.white_rooks | self.white_king

    def set_black_board(self):
        self.black_board = self.black_pawns | self.black_knights | self.black_bishops | self.black_queens | self.black_rooks | self.black_king

    def get_parsed_fen_piece_board(self):
        return self.piece_board

    def get_parsed_fen(self):
        return {
            "white_pawns": self.white_pawns,
            "black_pawns": self.black_pawns,
            "white_knights": self.white_knights,
            "black_knights": self.black_knights,
            "white_bishops": self.white_bishops,
            "black_bishops": self.black_bishops,
            "white_rooks": self.white_rooks,
            "black_rooks": self.black_rooks,
            "white_queens": self.white_queens,
            "black_queens": self.black_queens,
            "white_king": self.white_king,
            "black_king": self.black_king,
            "full_board": self.full_board,
            "white_board": self.white_board,
            "black_board": self.black_board,
            "side_to_move": self.color_to_move,
            "white_castle_kingside": self.white_castle_kingside,
            "white_castle_queenside": self.white_castle_queenside,
            "black_castle_kingside": self.black_castle_kingside,
            "black_castle_queenside": self.black_castle_queenside,
            "en_passant_target_square": self.en_passant_target_square,
            "color_to_move": self.color_to_move
        }
