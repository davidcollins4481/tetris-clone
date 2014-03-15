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

        # current piece under user's control
        self.current_piece = self.generator.next()

    def draw(self):
        row_number = 0;
        current_y = 0
        import pdb
        column_number = 0
        current_x = 0

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

        # re-draw board
        self.draw()

        # redraw pieces
        self.screen.blit(self.surface, (self.x, self.y))
        if not self.current_piece:
            self.current_piece = self.generator.next()

        self.current_piece.render(self.surface)
        self.screen.blit(self.surface, (self.x, self.y))

    def rotate_current(self):
        self.current_piece.rotate(self.surface)

    # kind of odd returning constants here..mehhh
    def row_height(self):
        return CELL_HEIGHT;

    def column_width(self):
        return CELL_WIDTH;

    # private methods 
    def _draw_previewer(self):
        self.previewer = PiecePreviewer(self.screen)
        self.previewer.draw()

