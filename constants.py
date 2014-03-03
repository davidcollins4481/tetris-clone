# width / height in pixels
SCREEN_SIZE = (600,800)
SCREEN_BGCOLOR = (0,0,0)

# PLAYFIELD CONSTANTS
# NOTE: the top two rows should not be visible
# tetris standard
ROWS = 22
COLUMNS = 10

# row height / column width
# try to make everything relative to SCREEN_SIZE...who knows -
# maybe we'll have to time to make it so you can change the game
# size

# make 5% of the screen width
CELL_WIDTH = SCREEN_SIZE[0] * .05

# 1px extra for the edge borders
PLAYFIELD_HEIGHT = (CELL_WIDTH * ROWS) + 1
PLAYFIELD_WIDTH = (CELL_WIDTH * COLUMNS) + 1

PLAYFIELD_BGCOLOR = (0,0,0)
GRID_LINE_COLOR = (111,111,111)
PLAYFIELD_BORDER_COLOR = (255,0,6)
FPS = 40

# preview constants
PREVIEWER_BGCOLOR = (100,100,100)
PREVIEWER_WIDTH = 120
PREVIEWER_HEIGHT = 120

# /PLAYFIELD CONSTANTS

