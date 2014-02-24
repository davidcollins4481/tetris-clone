from constants import *
from piece_previewer import *
import pygame

class Playfield:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width() - BORDER_WIDTH
        self.height = screen.get_height() - BORDER_WIDTH
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(PLAYFIELD_BGCOLOR)
        # want a large right margin for the piece previewer
        self.x = BORDER_WIDTH / 10
        self.y = BORDER_WIDTH / 2

    def draw(self):
        # '-2' is so the top 2 hidden rows are now accounted for when
        # considering height
        rowHeight = self.height / (ROWS - 2)
        rowNumber = 0;
        currentY = (rowHeight * 2) * - 1

        columnWidth = self.width / COLUMNS
        columnNumber = 0
        currentX = 0

        # draw rows
        while rowNumber < ROWS:
            pygame.draw.line(self.surface, GRID_LINE_COLOR, (0, currentY), (self.width, currentY))
            rowNumber = rowNumber + 1
            currentY = currentY + rowHeight

        # draw columns
        while columnNumber < COLUMNS:
            pygame.draw.line(self.surface, GRID_LINE_COLOR, (currentX, 0), (currentX, self.height))
            columnNumber = columnNumber + 1
            currentX = currentX + columnWidth

        self.screen.blit(self.surface, (self.x, self.y))
        self._drawPreviewer()

    def _drawPreviewer(self):
        self.previewer = PiecePreviewer(self.screen)
        self.previewer.draw()


