# width / height in pixels
SCREEN_SIZE = (600,800)
SCREEN_BGCOLOR = (255,255,255)

# PLAYFIELD CONSTANTS
# NOTE: the top two rows should not be visible
ROWS = 22
COLUMNS = 10

# row height / column width
# try to make everything relative to SCREEN_SIZE...who know
# maybe we'll have to time to make it so you can change the size
# for the screen
BORDER_WIDTH = 200
PLAYFIELD_HEIGHT = SCREEN_SIZE[1] - BORDER_WIDTH
PLAYFIELD_WIDTH = SCREEN_SIZE[0] - BORDER_WIDTH
ROW_HEIGHT = PLAYFIELD_HEIGHT / (ROWS - 2)
COLUMN_WIDTH = PLAYFIELD_WIDTH / COLUMNS

PLAYFIELD_BGCOLOR = (240, 248, 136)
GRID_LINE_COLOR = (0,0,0)
FPS = 40

# preview constants
PREVIEWER_BGCOLOR = (0,0,0)
PREVIEWER_WIDTH = 120
PREVIEWER_HEIGHT = 120

# /PLAYFIELD CONSTANTS

