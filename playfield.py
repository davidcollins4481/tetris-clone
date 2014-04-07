from constants import *
from piece_previewer import *
from tetrominos import RandomTetrominoGenerator

import pygame

class Playfield:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.Surface((PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT))
        self.surface.fill(PLAYFIELD_BGCOLOR)

        # want a large right margin for the piece previewer
        self.x = 0
        self.y = 0

        # temporary
        self.at_bottom = False

        self.generator = RandomTetrominoGenerator()

        # current piece under user's control
        self.current_piece = self.generator.next()

        # I would like to avoid the overhead of using an object to
        # represent a square if possible. Going to try to use values
        # 0 = empty square, 1 = not empty/not usable
        # start all off as empty
        # call like so: self.squares[row][column]

        # NOTE: I'm thinking that once a piece is settled in a location,
        # we can just set the color of the square to be that of the color 
        # of the piece which filled it. Are there any reasons that this wouldn't
        # work?
        self.squares = [[0 for x in xrange(COLUMNS)] for x in xrange(ROWS)]

    def draw(self):
        row_number = 0;
        current_y = 0
        column_number = 0
        current_x = 0


        # NOTE: these grid lines technically don't HAVE to be drawn.
        # they're nice now as guides to see during development, but
        # I'm guessing that they can be removed once we have pieces
        # moving/settling correctly. Should help a bit performance-wise

        # draw rows
        while row_number <= ROWS:
            line_color = GRID_LINE_COLOR
            if row_number == 0 or row_number == ROWS:
                line_color = PLAYFIELD_BORDER_COLOR

            pygame.draw.line(self.surface, line_color, (0, current_y), (PLAYFIELD_WIDTH, current_y))
            row_number = row_number + 1
            current_y = current_y + CELL_HEIGHT

        # draw columns
        while column_number <= COLUMNS:
            line_color = GRID_LINE_COLOR
            if column_number == 0 or column_number == COLUMNS:
                line_color = PLAYFIELD_BORDER_COLOR

            pygame.draw.line(self.surface, line_color, (current_x, 0), (current_x, PLAYFIELD_HEIGHT))
            column_number = column_number + 1
            current_x = current_x + CELL_WIDTH

        self.screen.blit(self.surface, (self.x, self.y))
        self._draw_previewer()

    def update(self):
        # paint over the surface with the background
        # color to wipe out previous render
        # This means that every piece will have to be
        # renderend every single time. This seemed to 
        # be the way to do it from what I've gathered - Dave
        self.surface.fill(SCREEN_BGCOLOR)

        # re-draw board with settled pieces
        self.draw()

        self.screen.blit(self.surface, (self.x, self.y))
        # would be great if the only thing this method did
        # was render the board and current piece. No code 
        # for the logic of when the next piece should be 
        # retrieved
#        if self.current_piece.top > CELL_HEIGHT*(ROWS-3):
#            self.current_piece = self.generator.next()

        self.current_piece.render(self.surface)
        self.screen.blit(self.surface, (self.x, self.y))

    def move_allowed(self, direction):
        # left = columns
        # top = rows
        # self.squares[row][column]
        row_offset = 0
        column_offset = 0

        if direction == LEFT:
            column_offset = -1
        elif direction == RIGHT:
            column_offset = 1
        elif direction == DOWN:
            row_offset = 1

        origin_row = (self.current_piece.top / CELL_HEIGHT) + row_offset
        origin_column = (self.current_piece.left / CELL_WIDTH) + column_offset
        pieces = self.current_piece.get_position_properties()

        # (left, top)
        # a dictionary will allow us to uniquify points
        # without extra computations since keys must be unique.
        squares = {}

        for piece in pieces:
            start_left = origin_column + piece['left']
            start_top = origin_row + piece['top']
            piece_width = int(piece['width']) / CELL_WIDTH
            piece_height = int(piece['height']) / CELL_HEIGHT

            # initial
            squares["{0},{1}".format(start_left, start_top)] = 1

            for i in range(piece_width):
                squares["{0},{1}".format(start_left + i, start_top)] = 1

            for i in range(piece_height):
                squares["{0},{1}".format(start_left, start_top + i)] = 1

        points = [point.split(',') for point in squares]
        print points

        # are we touching a side wall?
        if self.bound_by_wall(points):
            return False

        return True

    def bound_by_wall(self, points):
        for point in points:
            if int(point[0]) < 0 or int(point[0]) > COLUMNS - 1:
                return True

        return False

    def reached_bottom(self):
        # this is just temporary to test movements
        if self.at_bottom:
            # reset
            self.at_bottom = False
            return True
        else:
            return False

    def rotate_current(self):
        self.current_piece.rotate(self.surface)

    def record_current_piece_location(self):
        # TODO: store the location of the current piece in
        # self.squares
        return

    def get_next_piece(self):
        self.current_piece = self.generator.next()

    # processing key events
    def move_current(self, direction):
        # check if we're at the bottom - if so, record the location of the piece
        # and get next piece
        if self.reached_bottom():
            self.record_current_piece_location()
            self.get_next_piece()
            return

        if not self.move_allowed(direction):
            return

        # TODO: check if next movement is possible before performing it
        if direction == LEFT:
            self.current_piece.move_left()
        elif direction == RIGHT:
            self.current_piece.move_right()
        elif direction == DOWN:
            self.current_piece.move_down()

    # private methods 
    def _draw_previewer(self):
        self.previewer = PiecePreviewer(self.screen)
        self.previewer.draw()

