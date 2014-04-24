from constants import *
from tetrominos import RandomTetrominoGenerator
import random
import pygame

class Playfield:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.Surface((PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT))
        self.surface.fill(PLAYFIELD_BGCOLOR)

        # want a large right margin for the piece previewer
        self.x = int(PLAYFIELD_WIDTH * .075)
        self.y = int(PLAYFIELD_HEIGHT * .05)
        self.set_initial_game_state()

	pygame.mixer.music.load('Original Tetris Theme.mp3')
	pygame.mixer.music.play(-1) 
    def set_initial_game_state(self):
        # the lower this number is, the faster the pieces move
        self.level_delay = 40
        # if we end up adding levels, we should make the delay
        # be a function of the level number
        self.level = 1
        self.game_over_rendered = False
        self.game_over = False

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
        if self.is_game_over():
            self.draw_game_over()
        else:
            self.draw()
            self.screen.blit(self.surface, (self.x, self.y))
            self.current_tetromino.render(self.surface)
            self.screen.blit(self.surface, (self.x, self.y))

    # sending a direction to this (see constants LEFT, RIGHT, DOWN)
    # will get the locations AFTER that movement has been made.
    # Calling without a direction argument, will get the current
    # location
    def get_tetromino_locations(self, direction = 0, position=-1):
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

        if position != -1:
            pieces = self.current_tetromino.get_position_by_number(position)
        else:
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
            if self.no_more_moves(points):
                self.game_over = True

            return False

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
        # wallkicks
        next_position_number = self.current_tetromino.next_position() 
        next_position = self.current_tetromino.get_position_by_number(next_position_number)
        current_position = self.current_tetromino.get_position_properties()
        coords = self.current_tetromino.coords()

        left_key = lambda(p): p['left']
        farthest_right_key = lambda(p): p['width'] + p['left']

        #
        overage = 0
        ####
        # check for kick on left side
        ####

        # get the lowest left
        lowest_left_current = min(current_position, key=left_key)
        lowest_left_next    = min(next_position, key=left_key)

        if lowest_left_next['left']  < lowest_left_current['left']:
            if coords[1] < 0:
                # overages on the left side are defined in positive
                # terms...since the piece must move to the right
                overage = abs(coords[1]) / CELL_WIDTH

        ####
        # check for wallkicks on the right side
        ####

        # get the farthest right point for the current and next positions
        farthest_right_current = max(current_position, key=farthest_right_key)
        farthest_right_next    = max(next_position, key=farthest_right_key)
        # figure that the piece with the largest left/width is the farthest
        # right. Here we get the actual number for current/next positions
        r_current = farthest_right_current['left'] + farthest_right_current['width']
        r_next    = farthest_right_next['left'] + farthest_right_next['width']

        # if the next piece position will be farther right, we need to 
        # worry about wall kicks
        if r_next > r_current:
            # now that we've established that the next position is farther
            # to the right, let's make sure that piece is close to the wall
            next_position_width = farthest_right_next['total_width']
            r_overage = (CELL_WIDTH * COLUMNS) - (coords[1] + next_position_width)
            if r_overage < 0:
                overage = r_overage / CELL_WIDTH

        if overage == 0:
            if not self.is_rotation_possible(next_position_number):
                return

        self.current_tetromino.rotate(self.surface, overage)

    def is_rotation_possible(self, next_position_number, overage=0):
        points = self.get_tetromino_locations(0, next_position_number)

        if self.tetrominos_present(points):
            return False
        else:
            return True

    def store_tetromino(self):
        current_squares = self.get_tetromino_locations()
        # squares are stored [left,top] (think x,y)...
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

    def is_game_over(self):
        return self.game_over

    def draw_game_over(self):
        if self.game_over_rendered:
            return

        self.game_over_rendered = True

        colors = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

        for row in range(ROWS):
            for column in range(COLUMNS):
                pygame.draw.rect(self.surface, colors[random.randint(0,len(colors) - 1)], [
                    CELL_WIDTH * column,
                    CELL_HEIGHT * row,
                    CELL_WIDTH,
                    CELL_HEIGHT
                ])

        self.screen.blit(self.surface, (self.x, self.y))

        # render this on top of the board
        # x, y, width, height
        width = SCREEN_SIZE[0] * .80
        height = SCREEN_SIZE[1] * .40
        game_over_surface = pygame.Surface((width, height))

        game_over_surface.fill((255,255,255))

        pygame.draw.rect(game_over_surface, (0,0,0), [
            1,
            1,
            width - 2,
            height - 2
        ])

        # TODO: define font sizes as percentages of
        # screen dimensions
        font = pygame.font.SysFont(FONT, 60)
        label = font.render("Game Over!", 1, (255,255,0))

        game_over_surface.blit(label, (width * .25, height * .35))

        font = pygame.font.SysFont(FONT, 20)
        label = font.render("Press 'r' to play again", 1, (255,255,255))

        game_over_surface.blit(label, (width * .35, height * .55))

        x = (SCREEN_SIZE[0] / 2) - (width / 2)
        y = (SCREEN_SIZE[1] / 2) - (height / 2)
        self.screen.blit(game_over_surface, (x,y))

    def no_more_moves(self, points):

        for point in points:
            column,row = point[0],point[1]
            if row <= 1:
                return True

        return False

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
            if self.is_game_over():
                return
            else:
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

    def restart_game(self):
        self.screen.fill(SCREEN_BGCOLOR)
        self.set_initial_game_state()

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
class ScoreKeeper:
    def __init__(self, screen):

        self.x = int(SCREEN_SIZE[0] * .6)
        self.y = int(SCREEN_SIZE[1] * .50)

        self.score = 0
        self.screen = screen
        # [0] = 1 row, etc
        self.points = [40, 100, 300, 1200]

	self.scorefont = pygame.font.SysFont(FONT, 60)
	self.scoretext = self.scorefont.render(str(self.score), 1, (255,255,0))

        self.surface = pygame.Surface((PREVIEWER_WIDTH, PREVIEWER_HEIGHT))
        self.surface.fill(PREVIEWER_BGCOLOR)

	self.screen.blit(self.scoretext, (self.x, self.y))

    def draw(self):
        self.surface.fill(PREVIEWER_BGCOLOR)
        self.scoretext = self.scorefont.render(str(self.score), 1, (255,255,0))
        self.screen.blit(self.surface, (self.x, self.y))
	self.screen.blit(self.scoretext, (self.x, self.y))
	
    def update_score(self, level, deleted_rows):
        row_count_score = self.points[deleted_rows - 1]
        self.score += row_count_score * level

    def get_score(self):
        return self.score
