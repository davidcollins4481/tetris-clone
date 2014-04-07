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
        if self.current_piece.top > CELL_HEIGHT*(ROWS-3):
            self.current_piece = self.generator.next()

        self.current_piece.render(self.surface)
        self.screen.blit(self.surface, (self.x, self.y))

    def move_allowed(self):
        return True

    def reached_bottom(self):
        #self.current_piece
        return False;

    def rotate_current(self):
        self.current_piece.rotate(self.surface)

    def record_current_piece_location(self):
        # TODO: store the location of the current piece in
        # self.squares
        return

    def get_next_piece():
        self.current_piece = self.generator.next()

    # processing key events
    def move_current(self, direction):
        # check if we're at the bottom - if so, record the location of the piece
        # and get next piece
        if self.reached_bottom():
            self.record_current_piece_location()
            self.get_next_piece()
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
        self.previewer.draw()

