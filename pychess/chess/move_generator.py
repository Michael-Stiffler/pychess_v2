import numpy as np
import math
import cProfile
import pstats

SQUARES = [
    A8, B8, C8, D8, E8, F8, G8, H8,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A1, B1, C1, D1, E1, F1, G1, H1,
] = range(64)


class MoveGenerator:
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
        self.color_to_move = None
        self.white_castle_kingside = False
        self.black_castle_kingside = False
        self.white_castle_queenside = False
        self.black_castle_queenside = False
        self.en_passant_target_square = None
        self.knight_attack_squares = []
        self.rook_attack_square_mask = []
        self.king_attack_squares = []
        self.bishop_attack_square_mask = []
        self.pawn_attack_squares = [[], []]
        self.bishop_attack_squares = [[0] * 512 for _ in range(64)]
        self.rook_attack_squares = [[0] * 4096 for _ in range(64)]
        self.WHITE = 0
        self.BLACK = 1
        self.UNSIGNED_LONG_1 = np.ulonglong(1)
        self.not_ab_file = np.ulonglong(18229723555195321596)
        self.not_hg_file = np.ulonglong(4557430888798830399)
        self.not_h_file = np.ulonglong(9187201950435737471)
        self.not_a_file = np.ulonglong(18374403900871474942)
        self.rook_magics = [
            0xa8002c000108020,
            0x6c00049b0002001,
            0x100200010090040,
            0x2480041000800801,
            0x280028004000800,
            0x900410008040022,
            0x280020001001080,
            0x2880002041000080,
            0xa000800080400034,
            0x4808020004000,
            0x2290802004801000,
            0x411000d00100020,
            0x402800800040080,
            0xb000401004208,
            0x2409000100040200,
            0x1002100004082,
            0x22878001e24000,
            0x1090810021004010,
            0x801030040200012,
            0x500808008001000,
            0xa08018014000880,
            0x8000808004000200,
            0x201008080010200,
            0x801020000441091,
            0x800080204005,
            0x1040200040100048,
            0x120200402082,
            0xd14880480100080,
            0x12040280080080,
            0x100040080020080,
            0x9020010080800200,
            0x813241200148449,
            0x491604001800080,
            0x100401000402001,
            0x4820010021001040,
            0x400402202000812,
            0x209009005000802,
            0x810800601800400,
            0x4301083214000150,
            0x204026458e001401,
            0x40204000808000,
            0x8001008040010020,
            0x8410820820420010,
            0x1003001000090020,
            0x804040008008080,
            0x12000810020004,
            0x1000100200040208,
            0x430000a044020001,
            0x280009023410300,
            0xe0100040002240,
            0x200100401700,
            0x2244100408008080,
            0x8000400801980,
            0x2000810040200,
            0x8010100228810400,
            0x2000009044210200,
            0x4080008040102101,
            0x40002080411d01,
            0x2005524060000901,
            0x502001008400422,
            0x489a000810200402,
            0x1004400080a13,
            0x4000011008020084,
            0x26002114058042,
        ]

        self.bishop_magics = [
            0x89a1121896040240,
            0x2004844802002010,
            0x2068080051921000,
            0x62880a0220200808,
            0x4042004000000,
            0x100822020200011,
            0xc00444222012000a,
            0x28808801216001,
            0x400492088408100,
            0x201c401040c0084,
            0x840800910a0010,
            0x82080240060,
            0x2000840504006000,
            0x30010c4108405004,
            0x1008005410080802,
            0x8144042209100900,
            0x208081020014400,
            0x4800201208ca00,
            0xf18140408012008,
            0x1004002802102001,
            0x841000820080811,
            0x40200200a42008,
            0x800054042000,
            0x88010400410c9000,
            0x520040470104290,
            0x1004040051500081,
            0x2002081833080021,
            0x400c00c010142,
            0x941408200c002000,
            0x658810000806011,
            0x188071040440a00,
            0x4800404002011c00,
            0x104442040404200,
            0x511080202091021,
            0x4022401120400,
            0x80c0040400080120,
            0x8040010040820802,
            0x480810700020090,
            0x102008e00040242,
            0x809005202050100,
            0x8002024220104080,
            0x431008804142000,
            0x19001802081400,
            0x200014208040080,
            0x3308082008200100,
            0x41010500040c020,
            0x4012020c04210308,
            0x208220a202004080,
            0x111040120082000,
            0x6803040141280a00,
            0x2101004202410000,
            0x8200000041108022,
            0x21082088000,
            0x2410204010040,
            0x40100400809000,
            0x822088220820214,
            0x40808090012004,
            0x910224040218c9,
            0x402814422015008,
            0x90014004842410,
            0x1000042304105,
            0x10008830412a00,
            0x2520081090008908,
            0x40102000a0a60140,
        ]

        self.bishop_rellevant_bits = [
            6, 5, 5, 5, 5, 5, 5, 6,
            5, 5, 5, 5, 5, 5, 5, 5,
            5, 5, 7, 7, 7, 7, 5, 5,
            5, 5, 7, 9, 9, 7, 5, 5,
            5, 5, 7, 9, 9, 7, 5, 5,
            5, 5, 7, 7, 7, 7, 5, 5,
            5, 5, 5, 5, 5, 5, 5, 5,
            6, 5, 5, 5, 5, 5, 5, 6
        ]

        self.rook_rellevant_bits = [
            12, 11, 11, 11, 11, 11, 11, 12,
            11, 10, 10, 10, 10, 10, 10, 11,
            11, 10, 10, 10, 10, 10, 10, 11,
            11, 10, 10, 10, 10, 10, 10, 11,
            11, 10, 10, 10, 10, 10, 10, 11,
            11, 10, 10, 10, 10, 10, 10, 11,
            11, 10, 10, 10, 10, 10, 10, 11,
            12, 11, 11, 11, 11, 11, 11, 12
        ]

    def calculate_moves(self, color_to_move):
        bishop_occupancy = np.uint64(0)
        # bishop_occupancy = self.set_bit(bishop_occupancy, C5)
        # bishop_occupancy = self.set_bit(bishop_occupancy, F2)
        # bishop_occupancy = self.set_bit(bishop_occupancy, G7)
        # bishop_occupancy = self.set_bit(bishop_occupancy, B2)
        # bishop_occupancy = self.set_bit(bishop_occupancy, G5)
        # bishop_occupancy = self.set_bit(bishop_occupancy, E2)
        # bishop_occupancy = self.set_bit(bishop_occupancy, E7)
        # self.print_bitboard(bishop_occupancy)
        # self.print_bitboard(self.get_queen_attack_squares(D4, bishop_occupancy))

    def get_rook_attack_squares(self, square, occupancy):
        occupancy &= self.rook_attack_square_mask[square]
        occupancy *= np.uint64(self.rook_magics[square])
        occupancy >>= np.uint64(64) - np.uint64(self.rook_rellevant_bits[square])
        return self.rook_attack_squares[square][occupancy]

    def get_bishop_attack_squares(self, square, occupancy):

        occupancy &= self.bishop_attack_square_mask[square]
        occupancy *= np.uint64(self.bishop_magics[square])
        occupancy >>= np.uint64(64) - np.uint64(self.bishop_rellevant_bits[square])
        return self.bishop_attack_squares[square][occupancy]

    def get_queen_attack_squares(self, square, occupancy):
        attack_squares = np.uint64(0)

        bishop_occupancy = occupancy
        rook_occupancy = occupancy

        bishop_occupancy &= self.bishop_attack_square_mask[square]
        bishop_occupancy *= np.uint64(self.bishop_magics[square])
        bishop_occupancy >>= np.uint64(64) - np.uint64(self.bishop_rellevant_bits[square])

        attack_squares = self.bishop_attack_squares[square][bishop_occupancy]

        rook_occupancy &= self.rook_attack_square_mask[square]
        rook_occupancy *= np.uint64(self.rook_magics[square])
        rook_occupancy >>= np.uint64(64) - np.uint64(self.rook_rellevant_bits[square])

        attack_squares |= self.rook_attack_squares[square][rook_occupancy]

        return attack_squares

    def init(self, parsed_fen):
        self.set_important_values(parsed_fen)

        self.populate_knight_attack_squares()
        self.populate_pawn_attack_squares()
        self.populate_king_attack_squares()

        self.populate_bishop_attack_square_masks()
        self.init_bishop_magic_attacks()

        self.populate_rook_attack_square_masks()
        self.init_rook_magic_attacks()

        # Debugging stuff

        # with cProfile.Profile() as pr:
        # stats = pstats.Stats(pr)
        # stats.sort_stats(pstats.SortKey.TIME)
        # stats.print_stats()

    def set_important_values(self, fen):
        self.white_pawns = fen["white_pawns"]
        self.black_pawns = fen["black_pawns"]
        self.white_knights = fen["white_knights"]
        self.black_knights = fen["black_knights"]
        self.white_bishops = fen["white_bishops"]
        self.black_bishops = fen["black_bishops"]
        self.white_rooks = fen["white_rooks"]
        self.black_rooks = fen["black_rooks"]
        self.white_queens = fen["white_queens"]
        self.black_queens = fen["black_queens"]
        self.white_king = fen["white_king"]
        self.black_king = fen["black_king"]
        self.full_board = fen["full_board"]
        self.white_board = fen["white_board"]
        self.black_board = fen["black_board"]
        self.color_to_move = fen["color_to_move"]
        self.white_castle_kingside = fen["white_castle_kingside"]
        self.black_castle_kingside = fen["black_castle_kingside"]
        self.white_castle_queenside = fen["white_castle_queenside"]
        self.black_castle_queenside = fen["black_castle_queenside"]
        self.en_passant_target_square = fen["en_passant_target_square"]

    def init_rook_magic_attacks(self):
        for square in range(64):
            mask = self.rook_attack_square_mask[square]
            bits = self.count_bits(int(mask))
            variations = 1 << bits
            for variation in range(variations):
                occupancy = self.set_occupancy(variation, bits, mask)
                magic_index = (occupancy * np.uint64(self.rook_magics[square])) >> (np.uint(64) - np.uint64(self.rook_rellevant_bits[square]))
                self.rook_attack_squares[square][magic_index] = self.init_rook_attack_squares(square, occupancy)

    def init_bishop_magic_attacks(self):
        for square in range(64):
            mask = self.bishop_attack_square_mask[square]
            bits = self.count_bits(int(mask))
            variations = 1 << bits
            for variation in range(variations):
                occupancy = self.set_occupancy(variation, bits, mask)
                magic_index = (occupancy * np.uint64(self.bishop_magics[square])) >> (np.uint(64) - np.uint64(self.bishop_rellevant_bits[square]))
                self.bishop_attack_squares[square][magic_index] = self.init_bishop_attack_squares(square, occupancy)

    def populate_rook_attack_square_masks(self):

        for square in range(64):

            attack_squares = np.uint64(0)

            current_rank = math.floor(square / 8)
            current_file = square % 8

            desired_rank = current_rank + 1
            for _ in range(8):
                if desired_rank >= 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + current_file)))
                desired_rank += 1

            desired_rank = current_rank - 1
            for _ in range(8):
                if desired_rank <= 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + current_file)))
                desired_rank -= 1

            desired_file = current_file + 1
            for _ in range(8):
                if desired_file >= 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(current_rank * 8 + desired_file)))
                desired_file += 1

            desired_file = current_file - 1
            for _ in range(8):
                if desired_file <= 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(current_rank * 8 + desired_file)))
                desired_file -= 1

            self.rook_attack_square_mask.append(attack_squares)

    def init_rook_attack_squares(self, square, occupancy):
        attack_squares = np.uint64(0)

        current_rank = math.floor(square / 8)
        current_file = square % 8

        desired_rank = current_rank + 1
        for _ in range(8):
            if desired_rank > 7:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + current_file)))
            if occupancy & (np.uint64(1) << (np.uint64(desired_rank * 8 + current_file))):
                break
            desired_rank += 1

        desired_rank = current_rank - 1
        for _ in range(8):
            if desired_rank < 0:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + current_file)))
            if occupancy & (np.uint64(1) << (np.uint64(desired_rank * 8 + current_file))):
                break
            desired_rank -= 1

        desired_file = current_file + 1
        for _ in range(8):
            if desired_file > 7:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(current_rank * 8 + desired_file)))
            if occupancy & (np.uint64(1) << (np.uint64(current_rank * 8 + desired_file))):
                break
            desired_file += 1

        desired_file = current_file - 1
        for _ in range(8):
            if desired_file < 0:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(current_rank * 8 + desired_file)))
            if occupancy & (np.uint64(1) << (np.uint64(current_rank * 8 + desired_file))):
                break
            desired_file -= 1

        return attack_squares

    def init_bishop_attack_squares(self, square, occupancy):
        attack_squares = np.uint64(0)

        current_rank = math.floor(square / 8)
        current_file = square % 8

        desired_rank = current_rank + 1
        desired_file = current_file + 1
        for _ in range(8):
            if desired_rank > 7 or desired_file > 7:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
            if occupancy & (np.uint64(1) << (np.uint64(desired_rank * 8 + desired_file))):
                break
            desired_rank += 1
            desired_file += 1

        desired_rank = current_rank + 1
        desired_file = current_file - 1
        for _ in range(8):
            if desired_rank > 7 or desired_file < 0:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
            if occupancy & (np.uint64(1) << (np.uint64(desired_rank * 8 + desired_file))):
                break
            desired_rank += 1
            desired_file -= 1

        desired_rank = current_rank - 1
        desired_file = current_file + 1
        for _ in range(8):
            if desired_rank < 0 or desired_file > 7:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
            if occupancy & (np.uint64(1) << (np.uint64(desired_rank * 8 + desired_file))):
                break
            desired_rank -= 1
            desired_file += 1

        desired_rank = current_rank - 1
        desired_file = current_file - 1
        for _ in range(8):
            if desired_rank < 0 or desired_file < 0:
                break
            attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
            if occupancy & (np.uint64(1) << (np.uint64(desired_rank * 8 + desired_file))):
                break
            desired_rank -= 1
            desired_file -= 1

        return attack_squares

    def populate_bishop_attack_square_masks(self):

        for square in range(64):

            attack_squares = np.uint64(0)

            current_rank = math.floor(square / 8)
            current_file = square % 8

            desired_rank = current_rank + 1
            desired_file = current_file + 1
            for _ in range(8):
                if desired_rank >= 7 or desired_file >= 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank += 1
                desired_file += 1

            desired_rank = current_rank + 1
            desired_file = current_file - 1
            for _ in range(8):
                if desired_rank >= 7 or desired_file <= 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank += 1
                desired_file -= 1

            desired_rank = current_rank - 1
            desired_file = current_file + 1
            for _ in range(8):
                if desired_rank <= 0 or desired_file >= 7:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank -= 1
                desired_file += 1

            desired_rank = current_rank - 1
            desired_file = current_file - 1
            for _ in range(8):
                if desired_rank <= 0 or desired_file <= 0:
                    break
                attack_squares = attack_squares | (self.UNSIGNED_LONG_1 << (np.uint64(desired_rank * 8 + desired_file)))
                desired_rank -= 1
                desired_file -= 1

            self.bishop_attack_square_mask.append(attack_squares)

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
        return np.ulonglong(board) | (self.UNSIGNED_LONG_1 << np.ulonglong(index))

    def get_bit(self, board, square):
        return np.ulonglong(board) & (self.UNSIGNED_LONG_1 << np.ulonglong(square))

    def pop_bit(self, board, index):
        return np.ulonglong(board) ^ (self.UNSIGNED_LONG_1 << np.ulonglong(index)) if self.get_bit(board, index) else 0

    def count_bits(self, board):
        # count = 0
        # board = (np.uint64(board))
        # while (board):
        #     count += 1
        #     board &= board - np.uint64(1)
        # return count

        count = 0
        while (board):
            count += (board & 1)    # check last bit
            board >>= 1
        return count

    def get_least_sig_bit_index(self, board):
        if board:
            return self.count_bits(int((board & -board) - 1))
        else:
            return -1

    def set_occupancy(self, index, bits, mask):
        occupancy = np.uint64(0)
        for bit in range(bits):
            square = self.get_least_sig_bit_index(mask)
            mask = self.pop_bit(mask, square)

            if (index & (1 << bit)):
                occupancy |= (np.uint64(1) << np.uint64(square))

        return occupancy

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
