import pygame, sys
from pygame.locals import *
from playfield import *
from constants import *

def main():
    global screen, FPSCLOCK

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(SCREEN_BGCOLOR)
    
    pygame.display.set_caption('Tetris')

    playfield = Playfield(screen)
    playfield.draw()

    # this is the main game loop...this may get moved
    while True:
        FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    print "Rotate block"
                    playfield.rotate_current()

            # do this last
            playfield.update()

        pygame.display.update()

if __name__ == "__main__":
    main()
