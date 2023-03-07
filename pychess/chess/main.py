import numpy as np
from board import Board
from visuals import Visuals
import sys
import argparse
import pygame as py


def main():

    py.init()

    running = True
    need_to_calculate_moves = True
    holding_piece = False
    user_color = 0
    clock = py.time.Clock()

    args = get_args()

    board = Board()
    board.parse_fen(args.fen)
    board.set_printable_board()

    visuals = Visuals()
    visuals.load_pieces()
    visuals.draw_board()
    visuals.draw_pieces(board.get_printable_board())
    visuals.initialize_show_square()

    while running:
        mouse_pos = py.mouse.get_pos()
        visuals.show_square(mouse_pos)

        if holding_piece:
            visuals.draw_board()
            visuals.draw_moves()
            visuals.drag_piece(mouse_pos, board.get_board())

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                sys.exit()

        py.display.flip()
        py.display.update()

        clock.tick(30)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fen', '-f', '--fen', '--f',
                        dest='fen',
                        type=str,
                        help='FEN used to populate the board. Try "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" for the start position.')
    return parser.parse_args()


if __name__ == "__main__":
    main()
