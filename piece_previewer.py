from constants import *
import pygame
from tetrominos import RandomTetrominoGenerator

class PiecePreviewer:
    def __init__(self, screen, generator):
        self.screen = screen
        self.x = 450 
        self.y = 140
        self.surface = pygame.Surface((PREVIEWER_WIDTH, PREVIEWER_HEIGHT))
        self.surface.fill(PREVIEWER_BGCOLOR)
	self.generator = generator

    def draw(self):
	self.surface.fill(PREVIEWER_BGCOLOR)
        self.generator.sequence[0].render(self.surface)
	self.screen.blit(self.surface, (self.x, self.y)) 
