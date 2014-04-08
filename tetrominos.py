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
        self._generate_sequence()

    def next(self):
        # get the first
        next = self.sequence.pop(0)
        if not len(self.sequence):
            self._generate_sequence()

        return next

    def _generate_sequence(self):
	list = [1,2,3,4,5,6,7]
	random.shuffle(list)
	for x in list:
		self.sequence.append(TetrominoFactory.create_tetromino(x))

       #self.sequence = [ TetrominoFactory.create_tetromino(7) ]

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
    def create_tetromino(type):
        # only one type so far
        if type == 1:
            return Straight()
        elif type == 2:
            return Square()
        elif type == 3:
            return TShape()
        elif type == 4:
            return SShape()
	elif type == 5:
            return ZShape()
	elif type == 6:
	    return LGun()
	elif type == 7:
	    return RGun()
"""
See for details:
http://tetris.wikia.com/wiki/Tetromino

Here is our rotation system:
http://tetris.wikia.com/wiki/SRS
"""

class TetrominoPositionLogger(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, type=None):
        def wrapper(*args):
            print "Before: [{1}] {0}".format(obj.position_string(), obj.__class__)
            self.func(obj, *args)
            print "After:  [{1}] {0}".format(obj.position_string(), obj.__class__)

        return wrapper

class Tetromino(object):
    def __init__(self):
        # these should be specified in the 
        # child classes
        self.top = 0
        self.left = 0
        self.width = 0
        self.height = 0
        self.positions = []
        self.current_position = 0

    def render(self, surface):
        """ 
        override in specific classes. Each piece type
        has custom attributes - where it starts, how
        it turns, it's color, etc.
        """
        raise("Cannot use base implementation")

    def position_string(self):
        return "({0}, {1}) [position: {2}]".format(self.left, self.top, self.get_position_properties())

    def get_position_properties(self):
        return self.position_properties[self.current_position]

    def next_position(self):
        number_positions = len(self.positions)
        next = 0
        # we're on the last position
        if self.current_position == number_positions - 1:
            next = 0
        else:
            next = self.current_position + 1

        # leave it up to the caller to save this
        # info
        return next

    # this behavior seems generic enough to move here
    def rotate(self, surface):
        self.current_position = self.next_position()

    def move_left(self):
        self.left -= CELL_WIDTH

    def move_right(self):
        self.left += CELL_WIDTH

    def move_down(self):
        self.top += CELL_HEIGHT

class Straight(Tetromino):
    def __init__(self):
        super(Straight, self).__init__()
        self.positions = [0,1,2,3]

        # ok so all of the pieces are inside of a bounding box..
        # straights is a 4x4 box and the piece rotates within it.
        # there are four distinct positions for the straight piece
        # even though it seems as though there would only be two.
        self.position_properties = [
            [{ 'left': 0, 'top': 1, 'width': CELL_WIDTH * 4, 'height': CELL_HEIGHT     }],
            [{ 'left': 2, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 4 }],
            [{ 'left': 0, 'top': 2, 'width': CELL_WIDTH * 4, 'height': CELL_HEIGHT     }],
            [{ 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 4 }]
        ]

        self.current_position = 0

    # I'm hoping this method can be refactored into a single method
    # and placed in the base class
    def render(self, surface):
        # Rect(left, top, width, height)
        positions = self.position_properties[self.current_position]

        # NOTE: self.top and self.left will change with the user's/game's movements
        for position in positions:
            pygame.draw.rect(surface, CYAN, [
                self.left + (position['left'] * CELL_WIDTH),
                self.top + (position['top'] * CELL_HEIGHT),
                position['width'],
                position['height']
            ])

class Square(Tetromino):
    def __init__(self):
        super(Square, self).__init__()
        self.positions = [0]
        self.position_properties = [
            [{'left': 0, 'top': 0, 'width': CELL_WIDTH * 2 ,'height': CELL_HEIGHT * 2 }]
        ]

    def render(self, surface):
        # Rect(left, top, width, height)
        positions = self.position_properties[self.current_position]

        for piece_position in positions:
            pygame.draw.rect(surface, YELLOW, [
                self.left + (piece_position['left'] * CELL_WIDTH),
                self.top + (piece_position['top'] * CELL_HEIGHT),
                piece_position['width'],
                piece_position['height']
            ])

# lamest class name ever
class TShape(Tetromino):
    def __init__(self):
        super(TShape, self).__init__()
        # initial position is horizontal

        self.positions = [0,1,2,3]

        # t-shape is 3x3
        # drawing multiple shapes for each position
        self.position_properties = [
            [
                { 'left': 0, 'top': 1, 'width': CELL_WIDTH * 3, 'height': CELL_HEIGHT     },
                { 'left': 1 ,'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 3 },
                { 'left': 2, 'top': 1, 'width': CELL_WIDTH,     'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 0, 'top': 1, 'width': CELL_WIDTH * 3, 'height': CELL_HEIGHT     },
                { 'left': 1, 'top': 2, 'width': CELL_WIDTH,     'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 3 },
                { 'left': 0, 'top': 1, 'width': CELL_WIDTH,     'height': CELL_HEIGHT     }
            ]
        ]

        self.current_position = 0

    def render(self, surface):
        # Rect(left, top, width, height)
        positions = self.position_properties[self.current_position]

        for piece_position in positions:
            pygame.draw.rect(surface, PURPLE, [
                self.left + (piece_position['left'] * CELL_WIDTH),
                self.top + (piece_position['top'] * CELL_HEIGHT),
                piece_position['width'],
                piece_position['height']
            ])

class SShape(Tetromino):
    def __init__(self):
        super(SShape, self).__init__()
        # initial position is horizontal

        self.positions = [0,1,2,3]

        # s-shape bounding box is 4x4
        # drawing multiple shapes for each position
        self.position_properties = [
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     },
                { 'left': 0 ,'top': 1, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 },
                { 'left': 2, 'top': 1, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 }
            ],
            [
                { 'left': 1, 'top': 1, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     },
                { 'left': 0 ,'top': 2, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 0, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 },
                { 'left': 1, 'top': 1, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 }
            ]
        ]

        self.current_position = 0

    def render(self, surface):
        # Rect(left, top, width, height)
        positions = self.position_properties[self.current_position]

        for piece_position in positions:
            pygame.draw.rect(surface, GREEN, [
                self.left + (piece_position['left'] * CELL_WIDTH),
                self.top + (piece_position['top'] * CELL_HEIGHT),
                piece_position['width'],
                piece_position['height']
            ])

class ZShape(Tetromino):
    def __init__(self):
        super(ZShape, self).__init__()
        # initial position is horizontal

        self.positions = [0,1,2,3]

        # z-shape bounding box is 3x3
        # drawing multiple shapes for each position
        self.position_properties = [
            [
                { 'left': 0, 'top': 0, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     },
                { 'left': 1 ,'top': 1, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 2, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 },
                { 'left': 1, 'top': 1, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 }
            ],
            [
                { 'left': 0, 'top': 1, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     },
                { 'left': 1 ,'top': 2, 'width': CELL_WIDTH * 2, 'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 },
                { 'left': 0, 'top': 1, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 2 }
            ]
        ]

        self.current_position = 0

    def render(self, surface):
        # Rect(left, top, width, height)
        positions = self.position_properties[self.current_position]

        for piece_position in positions:
            pygame.draw.rect(surface, RED, [
                self.left + (piece_position['left'] * CELL_WIDTH),
                self.top + (piece_position['top'] * CELL_HEIGHT),
                piece_position['width'],
                piece_position['height']
            ])

class LGun(Tetromino):
    def __init__(self):
        super(LGun, self).__init__()
        # initial position is horizontal

        self.positions = [0,1,2,3]

        # left gun bounding box is 3x3
        # drawing multiple shapes for each position
        self.position_properties = [
            [
                { 'left': 0, 'top': 0, 'width': CELL_WIDTH, 'height': CELL_HEIGHT },
                { 'left': 0 ,'top': 1, 'width': CELL_WIDTH * 3, 'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH * 2,     'height': CELL_HEIGHT },
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 3 }
            ],
            [
                { 'left': 0, 'top': 1, 'width': CELL_WIDTH * 3, 'height': CELL_HEIGHT     },
                { 'left': 2 ,'top': 1, 'width': CELL_WIDTH, 'height': CELL_HEIGHT * 2 }
            ],
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 3 },
                { 'left': 0, 'top': 2, 'width': CELL_WIDTH * 2,     'height': CELL_HEIGHT }
            ]
        ]

        self.current_position = 0

    def render(self, surface):
        # Rect(left, top, width, height)
        positions = self.position_properties[self.current_position]

        for piece_position in positions:
            pygame.draw.rect(surface, BLUE, [
                self.left + (piece_position['left'] * CELL_WIDTH),
                self.top + (piece_position['top'] * CELL_HEIGHT),
                piece_position['width'],
                piece_position['height']
            ])

class RGun(Tetromino):
    def __init__(self):
        super(RGun, self).__init__()
        # initial position is horizontal

        self.positions = [0,1,2,3]

        # right gun bounding box is 3x3
        # drawing multiple shapes for each position
        self.position_properties = [
            [
                { 'left': 2, 'top': 0, 'width': CELL_WIDTH, 'height': CELL_HEIGHT },
                { 'left': 0 ,'top': 1, 'width': CELL_WIDTH * 3, 'height': CELL_HEIGHT     }
            ],
            [
                { 'left': 1, 'top': 2, 'width': CELL_WIDTH * 2,     'height': CELL_HEIGHT },
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 3 }
            ],
            [
                { 'left': 0, 'top': 1, 'width': CELL_WIDTH * 3, 'height': CELL_HEIGHT     },
                { 'left': 0 ,'top': 1, 'width': CELL_WIDTH, 'height': CELL_HEIGHT * 2 }
            ],
            [
                { 'left': 1, 'top': 0, 'width': CELL_WIDTH,     'height': CELL_HEIGHT * 3 },
                { 'left': 0, 'top': 0, 'width': CELL_WIDTH * 2,     'height': CELL_HEIGHT }
            ]
        ]

        self.current_position = 0

    def render(self, surface):
        # Rect(left, top, width, height)
        positions = self.position_properties[self.current_position]

        for piece_position in positions:
            pygame.draw.rect(surface, ORANGE, [
                self.left + (piece_position['left'] * CELL_WIDTH),
                self.top + (piece_position['top'] * CELL_HEIGHT),
                piece_position['width'],
                piece_position['height']
            ])
