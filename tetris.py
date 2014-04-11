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
    pygame.key.set_repeat(100, 10)
    # this is the main game loop...this may get moved
    piece_ticker = 0

    while True:
        FPSCLOCK.tick(FPS)

        piece_ticker += 1
        if piece_ticker == playfield.get_level_delay():
            playfield.move_current(DOWN)
            piece_ticker = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # it seems better to process key events here
            # rather than in the playfield class...if we moved
            # them from here, may be best to create a separate
            # class to manage the movements
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    playfield.rotate_current()
                elif event.key == K_LEFT:
                    playfield.move_current(LEFT)
                elif event.key == K_RIGHT:
                    playfield.move_current(RIGHT)
                elif event.key == K_DOWN:
                    playfield.move_current(DOWN)

            # do this last

        playfield.update()
        pygame.display.update()

if __name__ == "__main__":
    main()
