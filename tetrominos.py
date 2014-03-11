from constants import *
import pygame
import random # used to shuffle list of seven tetris blocks in tetromino
# this has to return the next piece to give to the user.
# the rules are here:
# http://tetris.wikia.com/wiki/Random_Generator
# it doesn't just draw one randomly - it finds 7.
# returns them then generates another i believe
class RandomTetrominoGenerator:
    def __init__(self):
        self.sequence = []
        self._generateSequence()

    def next(self):
        # get the first
        next = self.sequence.pop(0)
        if not len(self.sequence):
            self._generateSequence()

        return next

    def _generateSequence(self):
        self.sequence = [ TetrominoFactory.createTetromino() ] #Removed 1 argument because new method does not take any

class TetrominoFactory:
    """
    A factory used to control how tetrominos are made. For
    simplicity's sake, let's map each piece type to an integer:
        Pieces:
        1. = I = straight piece (color: cyan)
        2. = O = square piece (color: yellow)
        3. = T = t-shape piece (color: purple)
        4. = S = s-shape piece aka. "right snake" (color: green)
        5. = Z = z-shape piece aka. "left snake" (color: red)
        6. = J = left gun piece (color: blue)
        7. = L = right gun piece (color: orange)

       we can always map these to constant vars if needed. Ex: STRAIGHT = 1
   
    @staticmethod
    def createTetromino(type):
        # only one type so far
        if type == 1:
            return Straight()
        elif type == 2:
            return Square()

    Commented out this method because it returns a single block for tetromino.
    Algorithm is to return seven blocks, one of each, in random order.
    A very simplistic description of the algorithm linked to at the top
    of this page can be found here: http://www.tetrisconcept.net/forum/showthread.html?t=349
    First attempt is below.
   """
    @staticmethod
    def createTetromino():
        list = [1,2,3,4,5,6,7]
        random.shuffle(list)
        return list
"""
See for details:
http://tetris.wikia.com/wiki/Tetromino
"""

class Tetromino(object):
    def __init__(self):
        return

    def render(self, surface):
        """ 
        override in specific classes. Each piece type
        has custom attributes - where it starts, how
        it turns, it's color, etc.
        """
        raise("Cannot use base implementation")

class Straight(Tetromino):
    def __init__(self):
        super(Straight, self).__init__()

    def render(self, surface):
        # Rect(left, top, width, height)
        pygame.draw.rect(surface, CYAN, [0, 0, CELL_WIDTH * 4, CELL_HEIGHT])

    def rotate(self, surface):
        # FIXME: need to make sure "old" version is not rendered
        pygame.draw.rect(surface, CYAN, [0, 0, CELL_WIDTH, CELL_HEIGHT * 4])


class Square(Tetromino):
    def __init__(self):
        super(Square, self).__init__()

    def render(self, surface):
        # Rect(left, top, width, height)
        pygame.draw.rect(surface, YELLOW, [0, 0, CELL_WIDTH * 2, CELL_HEIGHT * 2])


