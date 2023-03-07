import pygame as py
import os
import math

# constants. self.SIZE is pixel LENGTH of each square on the board and LENGTH is how many squares per column or row.


class Visuals():
    def __init__(self):

        self.display = py.display.set_mode((800, 800))

        self.IMAGES = {}
        self.LENGTH = 8
        self.SIZE = 100

        # colors for black and white squares as well as the highlight color
        self.whiteColor = (255, 255, 255, 255)
        self.blackColor = (205, 129, 70, 255)
        self.highlight_color = (101, 67, 45, 140)

        self.current_user_square = None

        self.piece_held = None
        self.current_user_square = None
        self.board = []

        # set a pygame surface object for a square on the board with alpha and keep that square
        self.square_surface = py.Surface((100, 100), py.SRCALPHA)
        self.square_surface_rect = self.square_surface.get_rect(topleft=(0, 0))

    def draw_board(self):
        count = 0
        for x in range(1, self.LENGTH + 1):
            for y in range(1, self.LENGTH + 1):
                if count % 2 == 0:
                    py.draw.rect(self.display, self.whiteColor, [
                        self.SIZE*y - self.SIZE, self.SIZE*x - self.SIZE, self.SIZE, self.SIZE])
                else:
                    py.draw.rect(self.display, self.blackColor, [
                        self.SIZE*y - self.SIZE, self.SIZE*x - self.SIZE, self.SIZE, self.SIZE])
                count += 1
            count -= 1

    def load_pieces(self):
        pieces = ['bB', 'bK', 'bN', 'bP', 'bQ',
                  'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
        for piece in pieces:
            source_file_dir = os.path.dirname(os.path.abspath(os.getcwd()))
            image_path = os.path.join(
                source_file_dir, "piece_images\\" + piece + '.png')
            self.IMAGES[piece] = py.transform.scale(
                py.image.load(image_path), (self.SIZE, self.SIZE))

    def draw_pieces(self, board):
        self.board = board
        print(board)
        number_to_name_dict = {
            "8": 'bB',
            "11": 'bK',
            "7": 'bN',
            "6": 'bP',
            "10": 'bQ',
            "9": 'bR',
            "2": 'wB',
            "5": 'wK',
            "1": 'wN',
            "0": 'wP',
            "4": 'wQ',
            "3": 'wR'
        }

        for x in range(self.LENGTH):
            for y in range(self.LENGTH):
                position = (8 * x) + y
                piece = board[position]

                if piece is not None:
                    print(number_to_name_dict[str(piece)])
                    self.display.blit(self.IMAGES[number_to_name_dict[str(piece)]], py.Rect(
                        y * self.SIZE, x * self.SIZE, self.SIZE, self.SIZE))

    def drag_piece(self, mouse_pos, board):
        self.board = board
        for x in range(self.LENGTH):
            for y in range(self.LENGTH):
                piece = board[x][y]
                if piece == self.piece_held:
                    continue
                elif piece:
                    self.display.blit(self.IMAGES[piece.filename], py.Rect(
                        piece.x*self.SIZE, piece.y*self.SIZE, self.SIZE, self.SIZE))
        self.display.blit(
            self.IMAGES[self.piece_held.filename], (mouse_pos[0] - 50, mouse_pos[1] - 50))

    def draw_moves(self):
        moves = self.piece_held.moves_no_algebraic_notation
        for move in moves:
            py.draw.circle(self.display, self.highlight_color, [
                self.SIZE*(move[0] + 1) - (self.SIZE / 2), self.SIZE*(move[1] + 1) - (self.SIZE / 2)], 25)

    def initialize_show_square(self):
        py.draw.rect(self.square_surface, self.highlight_color,
                     self.square_surface_rect)
        self.display.blit(self.square_surface, self.square_surface_rect)

    def show_square(self, mouse_position):
        # this is for debugging purposes

        # formatted user position. ie (0,1), (2,2), etc
        square_postion_x, square_position_y = (math.floor(
            mouse_position[0] / self.SIZE), math.floor(mouse_position[1] / self.SIZE))

        # we want to check if the square the user is currently at is different than the last.
        # helps not run through this process if user hasn't moved cursor over current square.
        if self.current_user_square is None or self.current_user_square[0] != square_postion_x or self.current_user_square[1] != square_position_y:

            # draw the pieces and the board over what we have so it can reset each iteration
            self.draw_board()
            self.draw_pieces(self.board)

            # set the current_user_square to the one we just moved to
            self.current_user_square = (square_postion_x, square_position_y)
            # find and create the area around where the rectangle should be. ie (100,100), (300,400), etc.
            rect = (self.SIZE*(square_postion_x + 1) - self.SIZE, self.SIZE *
                    (square_position_y + 1) - self.SIZE, self.SIZE, self.SIZE)

            # change the current topleft of that rectange to those new values. draw that rectange with a color. blit it on screen.
            self.square_surface_rect.topleft = (rect[0], rect[1])
            self.display.blit(self.square_surface, self.square_surface_rect)
