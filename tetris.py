import pygame, sys
from pygame.locals import *
from playfield import *
from constants import *

def main():
    global screen, FPSCLOCK

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

        if not playfield.is_game_over():
            piece_ticker += 1
            if piece_ticker == playfield.get_level_delay():
                playfield.move_current(DOWN)
                piece_ticker = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if not playfield.is_game_over():
                    if event.key == K_SPACE or event.key == K_UP:
                        playfield.rotate_current()
                    elif event.key == K_LEFT:
                        playfield.move_current(LEFT)
                    elif event.key == K_RIGHT:
                        playfield.move_current(RIGHT)
                    elif event.key == K_DOWN:
                        playfield.move_current(DOWN)
                else:
                    # game is over..only allow restart
                    if event.key == K_r:
                        print "Restarting game"

        playfield.update()
        pygame.display.update()

if __name__ == "__main__":
    main()
