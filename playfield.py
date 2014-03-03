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
        self.x = 0#BORDER_WIDTH / 10
        self.y = 0#BORDER_WIDTH / 2

        self.generator = RandomTetrominoGenerator()

        # current piece under user's control
        self.current_piece = self.generator.next()

    def draw(self):
        rowNumber = 0;
        currentY = 0
        import pdb
        #pdb.set_trace()
        columnNumber = 0
        currentX = 0

        # draw rows
        while rowNumber <= ROWS:
            line_color = GRID_LINE_COLOR
            if rowNumber == 0 or rowNumber == ROWS:
#                pdb.set_trace()
                line_color = PLAYFIELD_BORDER_COLOR

            pygame.draw.line(self.surface, line_color, (0, currentY), (PLAYFIELD_WIDTH, currentY))
            rowNumber = rowNumber + 1
            currentY = currentY + CELL_WIDTH

        # draw columns
        while columnNumber <= COLUMNS:
            line_color = GRID_LINE_COLOR
            if columnNumber == 0 or columnNumber == COLUMNS:
                line_color = PLAYFIELD_BORDER_COLOR

            pygame.draw.line(self.surface, line_color, (currentX, 0), (currentX, PLAYFIELD_HEIGHT))
            columnNumber = columnNumber + 1
            currentX = currentX + CELL_WIDTH

        self.screen.blit(self.surface, (self.x, self.y))
        self._drawPreviewer()

    def update(self):
        if not self.current_piece:
            self.current_piece = self.generator.next()


    # kind of odd returning constants here..mehhh
    def rowHeight(self):
        return CELL_WIDTH;

    def columnWidth(self):
        return CELL_WIDTH;

    # private methods 
    def _drawPreviewer(self):
        self.previewer = PiecePreviewer(self.screen)
        self.previewer.draw()


