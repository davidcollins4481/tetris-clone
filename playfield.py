from constants import *
from tetrominos import RandomTetrominoGenerator

import pygame

class Playfield:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.Surface((PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT))
        self.surface.fill(PLAYFIELD_BGCOLOR)

        # the lower this number is, the faster the pieces move
        self.level_delay = 40
        # if we end up adding levels, we should make the delay
        # be a function of the level number
        self.level = 1
        # want a large right margin for the piece previewer
        self.x = int(PLAYFIELD_WIDTH * .075)
        self.y = int(PLAYFIELD_HEIGHT * .05)

        self.score_keeper = ScoreKeeper(self.screen)
        self.generator = RandomTetrominoGenerator()
        self.previewer = PiecePreviewer(self.screen, self.generator)

        # current piece under user's control
        self.current_tetromino = self.generator.next()

        # I would like to avoid the overhead of using an object to
        # represent a square if possible. Going to try to use values
        # 0 = empty square, 1 = not empty/not usable
        # start all off as empty
        # call like so: self.squares[column][row] (think x,y)

        # NOTE: I'm thinking that once a piece is settled in a location,
        # we can just set the color of the square to be that of the color 
        # of the piece which filled it. Are there any reasons that this wouldn't
        # work?
        self.squares = [[0 for x in xrange(ROWS)] for x in xrange(COLUMNS)]

    def draw(self):
        self.draw_board_lines()

        # draw blocks that are on board
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.squares[column][row]:
                    pygame.draw.rect(self.surface, self.squares[column][row]['color'], [
                        CELL_WIDTH * column,
                        CELL_HEIGHT * row,
                        CELL_WIDTH,
                        CELL_HEIGHT
                    ])

        self.screen.blit(self.surface, (self.x, self.y))
        self._draw_previewer()
        self._draw_score_keeper()

    def draw_board_lines(self):
        # draw vertical border
        pygame.draw.line(self.surface, PLAYFIELD_BORDER_COLOR, (0, 0), (0, ROWS * CELL_HEIGHT))
        pygame.draw.line(self.surface, PLAYFIELD_BORDER_COLOR, (COLUMNS * CELL_WIDTH, 0), (COLUMNS * CELL_WIDTH, ROWS * CELL_HEIGHT))

        # draw horizontal border
        pygame.draw.line(self.surface, PLAYFIELD_BORDER_COLOR, (0, 0), (COLUMNS * CELL_WIDTH, 0))

        pygame.draw.line(self.surface, PLAYFIELD_BORDER_COLOR, (0, ROWS * CELL_HEIGHT), (COLUMNS * CELL_WIDTH, ROWS * CELL_HEIGHT))

    def update(self):
        # paint over the surface with the background
        # color to wipe out previous render
        # This means that every piece will have to be
        # renderend every single time. This seemed to 
        # be the way to do it from what I've gathered - Dave
        self.surface.fill(SCREEN_BGCOLOR)

        # re-draw board with settled pieces
        self.draw()

        self.screen.blit(self.surface, (self.x, self.y))
        # would be great if the only thing this method did
        # was render the board and current piece. No code 
        # for the logic of when the next piece should be 
        # retrieved
#        if self.current_tetromino.top > CELL_HEIGHT*(ROWS-3):
#            self.current_tetromino = self.generator.next()

        self.current_tetromino.render(self.surface)
        self.screen.blit(self.surface, (self.x, self.y))

    # sending a direction to this (see constants LEFT, RIGHT, DOWN)
    # will get the locations AFTER that movement has been made.
    # Calling without a direction argument, will get the current
    # location
    def get_tetromino_locations(self, direction = 0):
        row_offset = 0
        column_offset = 0

        if direction == LEFT:
            column_offset = -1
        elif direction == RIGHT:
            column_offset = 1
        elif direction == DOWN:
            row_offset = 1

        origin_row = (self.current_tetromino.top / CELL_HEIGHT) + row_offset
        origin_column = (self.current_tetromino.left / CELL_WIDTH) + column_offset
        pieces = self.current_tetromino.get_position_properties()

        # (left, top)
        # a dictionary will allow us to uniquify points
        # without extra computations since keys must be unique.
        squares = {}

        for piece in pieces:
            start_left = origin_column + piece['left']
            start_top = origin_row + piece['top']
            piece_width = int(piece['width']) / CELL_WIDTH
            piece_height = int(piece['height']) / CELL_HEIGHT

            # initial
            squares["{0},{1}".format(start_left, start_top)] = 1

            for i in range(piece_width):
                squares["{0},{1}".format(start_left + i, start_top)] = 1

            for i in range(piece_height):
                squares["{0},{1}".format(start_left, start_top + i)] = 1

        return [map(lambda(x): int(x), point.split(',')) for point in squares]

    def move_allowed(self, direction):
        points = self.get_tetromino_locations(direction)

        # are we touching a side wall?
        if self.bound_by_wall(points):
            return False

        if self.tetrominos_present(points):
            return False

        #print points
        return True

    def tetrominos_present(self, points):
        for point in points:
            if self.squares[ point[0] ][ point[1] ]:
                return True

    def bound_by_wall(self, points):
        for point in points:
            if point[0] < 0 or point[0] > COLUMNS - 1:
                return True

        return False

    def reached_bottom(self):
        points = self.get_tetromino_locations()
        bottom_points = filter(lambda point: point[1] == ROWS - 1, points)
        if len(bottom_points) == 0:
            return False
        else:
            return True

    def rotate_current(self):
        self.current_tetromino.rotate(self.surface)

    def store_tetromino(self):
        # TODO: store the location of the current piece in
        # self.squares
        current_squares = self.get_tetromino_locations()
        # squares are stored [left,top] (think x,y)...
        # 
        for square in current_squares:
            self.squares[ square[0] ][ square[1] ] = { 'color': self.current_tetromino.color }

    def get_next_tetromino(self):
        self.current_tetromino = self.generator.next()

    def complete_tetromino_movement(self):
        self.store_tetromino()
        # check for completed lines to remove
        self.destroy_completed_lines()
        self.get_next_tetromino()

    def destroy_completed_lines(self):
        # call like so: self.squares[column][row] (think x,y)
        deleted_rows = 0
        for row in range(ROWS):
            # get the row's columns
            columns = [self.squares[column][row] for column in range(COLUMNS)]

            # get all empty squares...if none are returned, the row
            # is filled
            filled = len(filter(lambda(c): not c, columns)) == 0

            if filled:
                deleted_rows += 1

                for c in range(COLUMNS):
                    self.squares[c][row] = 0

                # TODO: Move all pieces above deleted row down a row
                for row_number in range(row, 0, -1):
                    for c in range(COLUMNS):
                        self.squares[c][row_number] = self.squares[c][row_number - 1]

        if deleted_rows > 0:
            self.score_keeper.update_score(self.level, deleted_rows)


    # processing key events
    def move_current(self, direction):
        # piece has reached the bottom of the board.
        # Store it
        if self.reached_bottom():
            self.complete_tetromino_movement()
            return

        allowed = self.move_allowed(direction)

        # piece is as far down as it can go
        if not allowed and direction == DOWN:
            self.complete_tetromino_movement()
            return

        # otherwise we're dealing with a side-to-side movement
        if not allowed:
            return

        if direction == LEFT:
            self.current_tetromino.move_left()
        elif direction == RIGHT:
            self.current_tetromino.move_right()
        elif direction == DOWN:
            self.current_tetromino.move_down()

    def get_level_delay(self):
        return self.level_delay

    # private methods 
    def _draw_previewer(self):
        self.previewer.draw()

    def _draw_score_keeper(self):
        self.score_keeper.draw()

class PiecePreviewer:
    def __init__(self, screen, generator):
        self.screen = screen
        self.x = int(SCREEN_SIZE[0] * .6)
        self.y = int(SCREEN_SIZE[1] * .23)
        self.surface = pygame.Surface((PREVIEWER_WIDTH, PREVIEWER_HEIGHT))
        self.surface.fill(PREVIEWER_BGCOLOR)
	self.generator = generator

    def draw(self):
	self.surface.fill(PREVIEWER_BGCOLOR)
        self.generator.sequence[0].render(self.surface)
	self.screen.blit(self.surface, (self.x, self.y)) 

# we're going to score luke the Original Nintendo
# version of the game did
# http://tetris.wikia.com/wiki/Scoring

# TODO
# these should change...basically just copied in from preview code
class ScoreKeeper:
    def __init__(self, screen):

        self.x = int(SCREEN_SIZE[0] * .6)
        self.y = int(SCREEN_SIZE[1] * .50)

        self.score = 0
        self.screen = screen
        # [0] = 1 row, etc
        self.points = [40, 100, 300, 1200]

        self.surface = pygame.Surface((PREVIEWER_WIDTH, PREVIEWER_HEIGHT))
        self.surface.fill(PREVIEWER_BGCOLOR)

    def draw(self):
        self.surface.fill(PREVIEWER_BGCOLOR)
        self.screen.blit(self.surface, (self.x, self.y))

    def update_score(self, level, deleted_rows):
        row_count_score = self.points[deleted_rows - 1]
        self.score += row_count_score * level
        print "Score: {0}".format(self.score)

    def get_score(self):
        return self.score
