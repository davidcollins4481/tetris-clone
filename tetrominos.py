class TetrominoFactory:
    """ A factory used to control how tetrominos are made """
    @staticmethod
    def createTetromino(type):
        return

"""
See for details:
http://tetris.wikia.com/wiki/Tetromino
"""

class Tetromimno:
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


"""
Pieces:
I = straight piece (color: cyan)
O = square piece (color: yellow)
T = t-shape piece (color: purple)
S = s-shape piece aka. "right snake" (color: green)
Z = z-shape piece aka. "left snake" (color: red)
J = left gun piece (color: blue)
L = right gun piece (color: orange)

"""
