from constants import *
import pygame

class PiecePreviewer:
    def __init__(self, screen):
        self.screen = screen
        self.x = 450 
        self.y = 140
        self.surface = pygame.Surface((PREVIEWER_WIDTH, PREVIEWER_HEIGHT))
        self.surface.fill(PREVIEWER_BGCOLOR)

    def draw(self):
        self.screen.blit(self.surface, (self.x, self.y))
