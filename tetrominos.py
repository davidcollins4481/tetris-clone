
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
        self.sequence = [ TetrominoFactory.createTetromino(1) ]

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
    """
    @staticmethod
    def createTetromino(type):
        # only one type so far
        if type == 1:
            return Straight()

"""
See for details:
http://tetris.wikia.com/wiki/Tetromino
"""

class Tetromino(object):
    def __init__(self):
        return

    def render(self, screen):
        """ 
        override in specific classes. Each piece type
        has custom attributes - where it starts, how
        it turns, it's color, etc.
        """
        raise("Cannot use base implementation")

class Straight(Tetromino):
    def __init__(self):
        super(Straight, self).__init__()

    def render(self, screen):
        return
