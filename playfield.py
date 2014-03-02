from constants import *
from piece_previewer import *
import pygame

class Playfield:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.Surface((PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT))
        self.surface.fill(PLAYFIELD_BGCOLOR)

        # want a large right margin for the piece previewer
        self.x = BORDER_WIDTH / 10
        self.y = BORDER_WIDTH / 2

    def draw(self):
        # '-2' is so the top 2 hidden rows are now accounted for when
        # considering height
        rowNumber = 0;
        currentY = (ROW_HEIGHT * 2) * - 1

        columnNumber = 0
        currentX = 0

        # draw rows
        while rowNumber < ROWS:
            pygame.draw.line(self.surface, GRID_LINE_COLOR, (0, currentY), (PLAYFIELD_WIDTH, currentY))
            rowNumber = rowNumber + 1
            currentY = currentY + ROW_HEIGHT

        # draw columns
        while columnNumber < COLUMNS:
            pygame.draw.line(self.surface, GRID_LINE_COLOR, (currentX, 0), (currentX, PLAYFIELD_HEIGHT))
            columnNumber = columnNumber + 1
            currentX = currentX + COLUMN_WIDTH

        self.screen.blit(self.surface, (self.x, self.y))
        self._drawPreviewer()

    # kind of odd returning constants here..mehhh
    def rowHeight(self):
        return ROW_HEIGHT;

    def columnWidth(self):
        return COLUMN_WIDTH;

    # private methods 
    def _drawPreviewer(self):
        self.previewer = PiecePreviewer(self.screen)
        self.previewer.draw()


