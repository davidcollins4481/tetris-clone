# width / height in pixels
SCREEN_SIZE = (600,800)
SCREEN_BGCOLOR = (0,0,0)

# PLAYFIELD CONSTANTS
# NOTE: the top two rows should not be visible
# tetris standard
ROWS = 22
COLUMNS = 10

# DIRECTIONS
LEFT = 1
RIGHT = 2
DOWN = 3

# row height / column width
# try to make everything relative to SCREEN_SIZE...who knows -
# maybe we'll have to time to make it so you can change the game
# size

# make 5% of the screen width
CELL_WIDTH = int(SCREEN_SIZE[0] * .05)
# improves readability
CELL_HEIGHT = CELL_WIDTH
# 1px extra for the edge borders
PLAYFIELD_HEIGHT = (CELL_WIDTH * ROWS) + 1
PLAYFIELD_WIDTH = (CELL_WIDTH * COLUMNS) + 1

PLAYFIELD_BGCOLOR = (0,0,0)
GRID_LINE_COLOR = (0,0,0)
PLAYFIELD_BORDER_COLOR = (255,0,6)
FPS = 40

# preview constants
PREVIEWER_BGCOLOR = (100,100,100)
PREVIEWER_WIDTH = 120
PREVIEWER_HEIGHT = 120

# /PLAYFIELD CONSTANTS

# Tetromino colors
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
