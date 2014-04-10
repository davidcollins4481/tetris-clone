from constants import *
import pygame
from tetrominos import RandomTetrominoGenerator

class PiecePreviewer:
    def __init__(self, screen):
        self.screen = screen
        self.x = 450 
        self.y = 140
        self.surface = pygame.Surface((PREVIEWER_WIDTH, PREVIEWER_HEIGHT))
        self.surface.fill(PREVIEWER_BGCOLOR)
	self.generator = RandomTetrominoGenerator()

    def draw(self):
        self.screen.blit(self.surface, (self.x, self.y))
	self.generator.sequence[-1].render(self.surface)
