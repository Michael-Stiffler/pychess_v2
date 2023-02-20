import numpy as np
from board import Board
import sys
import argparse


def main():
    args = get_args()
    board = Board()
    board.parse_fen(args.fen)
    board.print_board()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fen', '-f', '--fen', '--f',
                        dest='fen',
                        type=str,
                        help='FEN used to populate the board. Try "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" for the start position.')
    return parser.parse_args()


if __name__ == "__main__":
    main()
