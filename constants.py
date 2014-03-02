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

# FIXME: this 'BORDER_WIDTH' is stupid :) needs
# removed and substituted with something else when all
# major layout sections are in place
BORDER_WIDTH = SCREEN_SIZE[0] / 3
PLAYFIELD_HEIGHT = SCREEN_SIZE[1] - BORDER_WIDTH
PLAYFIELD_WIDTH = SCREEN_SIZE[0] - BORDER_WIDTH
# '-2' is so the top 2 hidden rows are now accounted for when
# considering height
ROW_HEIGHT = PLAYFIELD_HEIGHT / (ROWS - 2)
COLUMN_WIDTH = PLAYFIELD_WIDTH / COLUMNS

PLAYFIELD_BGCOLOR = (0,0,0)
GRID_LINE_COLOR = (111,111,111)
PLAYFIELD_BORDER_COLOR = (255,0,6)
FPS = 40

# preview constants
PREVIEWER_BGCOLOR = (100,100,100)
PREVIEWER_WIDTH = 120
PREVIEWER_HEIGHT = 120

# /PLAYFIELD CONSTANTS

