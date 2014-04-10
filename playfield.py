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

        self.generator = RandomTetrominoGenerator()
        self.previewer = PiecePreviewer(self.screen)

        # current piece under user's control
        self.current_tetromino = self.generator.next()

        # I would like to avoid the overhead of using an object to
        # represent a square if possible. Going to try to use values
        # 0 = empty square, 1 = not empty/not usable
        # start all off as empty
        # call like so: self.squares[column][row] (think x,y)

        # NOTE: I'm thinking that once a piece is settled in a location,
        # we can just set the color of the square to be that of the color 
        # of the piece which filled it. Are there any reasons that this wouldn't
        # work?
        self.squares = [[0 for x in xrange(ROWS)] for x in xrange(COLUMNS)]

    def draw(self):
        self.draw_board_lines()

        # draw blocks that are on board
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.squares[column][row]:
                    pygame.draw.rect(self.surface, self.squares[column][row]['color'], [
                        CELL_WIDTH * column,
                        CELL_HEIGHT * row,
                        CELL_WIDTH,
                        CELL_HEIGHT
                    ])

        self.screen.blit(self.surface, (self.x, self.y))
        self._draw_previewer()

    def draw_board_lines(self):
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
#        if self.current_tetromino.top > CELL_HEIGHT*(ROWS-3):
#            self.current_tetromino = self.generator.next()

        self.current_tetromino.render(self.surface)
        self.screen.blit(self.surface, (self.x, self.y))

    # sending a direction to this (see constants LEFT, RIGHT, DOWN)
    # will get the locations AFTER that movement has been made.
    # Calling without a direction argument, will get the current
    # location
    def get_tetromino_locations(self, direction = 0):
        row_offset = 0
        column_offset = 0

        if direction == LEFT:
            column_offset = -1
        elif direction == RIGHT:
            column_offset = 1
        elif direction == DOWN:
            row_offset = 1

        origin_row = (self.current_tetromino.top / CELL_HEIGHT) + row_offset
        origin_column = (self.current_tetromino.left / CELL_WIDTH) + column_offset
        pieces = self.current_tetromino.get_position_properties()

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

        return [map(lambda(x): int(x), point.split(',')) for point in squares]

    def move_allowed(self, direction):
        points = self.get_tetromino_locations(direction)

        # are we touching a side wall?
        if self.bound_by_wall(points):
            return False

        if self.tetrominos_present(points):
            return False

        #print points
        return True

    def tetrominos_present(self, points):
        for point in points:
            if self.squares[ point[0] ][ point[1] ]:
                return True

    def bound_by_wall(self, points):
        for point in points:
            if point[0] < 0 or point[0] > COLUMNS - 1:
                return True

        return False

    def reached_bottom(self):
        points = self.get_tetromino_locations()
        bottom_points = filter(lambda point: point[1] == ROWS - 1, points)
        if len(bottom_points) == 0:
            return False
        else:
            return True

    def rotate_current(self):
        self.current_tetromino.rotate(self.surface)

    def store_tetromino(self):
        # TODO: store the location of the current piece in
        # self.squares
        current_squares = self.get_tetromino_locations()
        # squares are stored [left,top] (think x,y)...
        # 
        for square in current_squares:
            self.squares[ square[0] ][ square[1] ] = { 'color': self.current_tetromino.color }

    def get_next_tetromino(self):
        self.current_tetromino = self.generator.next()

    # processing key events
    def move_current(self, direction):
        # piece has reached the bottom of the board.
        # Store it
        if self.reached_bottom():
            self.store_tetromino()
            self.get_next_tetromino()
            return

        allowed = self.move_allowed(direction)

        # piece is as far down as it can go
        if not allowed and direction == DOWN:
            self.store_tetromino()
            self.get_next_tetromino()
            return

        if not allowed:
            return

        if direction == LEFT:
            self.current_tetromino.move_left()
        elif direction == RIGHT:
            self.current_tetromino.move_right()
        elif direction == DOWN:
            self.current_tetromino.move_down()

    # private methods 
    def _draw_previewer(self):
        self.previewer.draw()

