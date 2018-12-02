
from pygame.locals import *
from random import randint
import pygame
import sys


'''
Defines a set of global variables.
'''

BLACK = (0, 0, 0)               # Empty
WHITE = (255, 255, 255)         # Wall
YELLOW = (255, 255, 0)          # Fruits
BLUE = (0, 0, 255)              # Monster
RED = (255, 0, 0)               # Player

UP = 0                          # Move up
DOWN = 1                        # Move down
LEFT = 2                        # Move left
RIGHT = 3                       # Move right


'''
Defines a class names Maze. Maze is the main place for the game to happens
'''


class Maze:

    size = [500, 260]   # 15 rows, 25 cols.
    step = 20
    MAX_ROW = 13
    MAX_COL = 25

    screen = None
    wall = []
    food = []

    # Initialize the maze (parameters)

    def __init__(self):

        self.on_init()
        self.on_set_wall()
        self.on_set_food()

    # Initialize the maze (set up screens)

    def on_init(self):

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Simple PacMan")

    # Initialize the maze. Use a 2D array of 0 and 1. 1 represents a wall

    def on_set_wall(self):

        self.wall.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.wall.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.wall.append([1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1])
        self.wall.append([1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1])
        self.wall.append([1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1])
        self.wall.append([1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1])
        self.wall.append([1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1])
        self.wall.append([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1])
        self.wall.append([1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1])
        self.wall.append([1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1])
        self.wall.append([1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1])
        self.wall.append([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        self.wall.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    # When there is no wall, place there foods.

    def on_set_food(self):
        self.food =[[0 for i in range(0, self.MAX_COL)] for j in range(0, self.MAX_ROW)]
        for i in range(0, self.MAX_ROW):
            for j in range(0, self.MAX_COL):
                if self.wall[i][j] == 0:
                    self.food[i][j] = 1

    # When there is food on ground, eat it.

    def on_consume_food(self, rows, cols):

        if self.food[rows][cols] == 1:
            self.food[rows][cols] = 0

    # use color white to draw walls, use color yellow to draw food. They are rectangles.

    def on_draw_wall(self):

        for i in range(0, self.MAX_ROW):
            for j in range(0, self.MAX_COL):
                if self.wall[i][j] == 1:
                    pygame.draw.rect(self.screen, WHITE, [j*self.step, i*self.step, self.step, self.step])
                    # Rect is a object: (x,y,width,height)

                if self.food[i][j] == 1:
                    pygame.draw.rect(self.screen, YELLOW, [j*self.step+7, i*self.step+7, 5, 5])

'''
Defines a super class actor
'''


class Actor(Maze):

    rows = 0
    cols = 0

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

    # A helper function to check whether a certain grid is wall.

    def is_wall(self, rows, cols, map):

        if map.wall[rows][cols] == 1:
            return True
        else:
            return False

    # move character left. if the character is human, consume food.

    def move_left(self, map, mode):

        if not self.is_wall(self.rows, self.cols - 1, map):
            if mode == 0:
                map.on_consume_food(self.rows, self.cols - 1)
            self.cols = self.cols - 1

    # move character right. if the character is human, consume food.

    def move_right(self, map, mode):

        if not self.is_wall(self.rows, self.cols + 1, map):
            if mode == 0:
                map.on_consume_food(self.rows, self.cols + 1)
            self.cols = self.cols + 1

    # move character up. if the character is human, consume food.

    def move_up(self, map, mode):

        if not self.is_wall(self.rows - 1, self.cols, map):
            if mode == 0:
                map.on_consume_food(self.rows - 1, self.cols)
            self.rows = self.rows - 1

    # move character down. if the character is human, consume food.

    def move_down(self, map, mode):
        if mode == 0:
            map.on_consume_food(self.rows + 1, self.cols)
        if not self.is_wall(self.rows + 1, self.cols, map):
            self.rows = self.rows + 1


'''
Defines a class Player inherit Actor
'''


class Player(Actor):

    # initialize player at random position

    def __init__(self, map):

        rows = randint(0, self.MAX_ROW - 1)
        cols = randint(0, self.MAX_COL - 1)

        while self.is_wall(rows, cols, map):
            rows = randint(0, self.MAX_ROW - 1)
            cols = randint(0, self.MAX_COL - 1)

        Actor.__init__(self, rows, cols)

    # move player left.

    def player_move_left(self,map):

        Actor.move_left(self, map.wall, 0)

    # move player right.

    def player_move_right(self, map):

        Actor.move_right(self, map.wall, 0)

    # move player up.

    def player_move_up(self, map):

        Actor.move_up(self, map.wall, 0)

    # move player down

    def player_move_down(self, map):

        Actor.move_down(self, map.wall, 0)

    # display player at windows. player is a red circle.

    def display(self, map):
        pygame.draw.circle(map.screen, RED, (self.cols * map.step + 10, self.rows * map.step + 10), 7)


'''
Defines a monster Player inherit Actor
'''


class Monster(Actor):

    direction = 0
    found_player = False
    escape_player = False

    # initialize player at random position and assign it with a proper direction

    def __init__(self, map):

        rows = randint(0, self.MAX_ROW - 1)
        cols = randint(0, self.MAX_COL - 1)

        while self.is_wall(rows, cols, map):
            rows = randint(0, self.MAX_ROW - 1)
            cols = randint(0, self.MAX_COL - 1)

        Actor.__init__(self, rows, cols)

        if not self.is_wall(rows, cols - 1, map):
            self.direction = LEFT
        elif not self.is_wall(rows, cols + 1, map):
            self.direction = RIGHT
        elif not self.is_wall(rows - 1, cols, map):
            self.direction = UP
        else:
            self.direction = DOWN

    # helper function to check whether monster is at a cross (more than two direction to go at a specific point.)

    def is_at_cross(self, map):

        count = 0

        if not self.is_wall(self.rows - 1, self.cols, map):
            count += 1
        if not self.is_wall(self.rows + 1, self.cols, map):
            count += 1
        if not self.is_wall(self.rows, self.cols - 1, map):
            count += 1
        if not self.is_wall(self.rows, self.cols + 1, map):
            count += 1

        if count > 2:
            return True
        else:
            return False

    # check whether the monster is at a corner. (two way (not in a line) to go)

    def is_at_corner(self, map):

        if self.is_wall(self.rows + 1, self.cols, map) and (self.is_wall(self.rows, self. cols + 1, map) or self.is_wall(self.rows, self. cols - 1, map)):
            return True

        if self.is_wall(self.rows - 1, self.cols, map) and (self.is_wall(self.rows, self. cols + 1, map) or self.is_wall(self.rows, self. cols - 1, map)):
            return True

        return False

    # check whether player is spotted by monster. if yes, the monster will chase the player.

    def seek(self, player):

        if abs(self.rows - player.rows) + abs(self.cols - player.cols) < 12:
            self.found_player = True
        else:
            self.found_player = False

    # the chase algorithms. when the monster chase, it has 50% odd tp choose a random direction.
    # the remaining 50% odd the monster will try to approach the player by reducing their difference
    # in the coordinate. If target direction is a wall, the monster will them choose a random dir.

    def chase(self, player, map):

        odd = randint(0, 2)

        if odd == 0 or odd == 1: # need to check target direction wall?
            return self.random_direction(map)
        else:
            if self.rows < player.rows and not self.is_wall(self.rows + 1, self.cols, map):
                return DOWN
            elif self.rows > player.rows and not self.is_wall(self.rows - 1, self.cols, map):
                return UP
            elif self.cols < player.cols and not self.is_wall(self.rows, self.cols + 1, map):
                return RIGHT
            elif self.cols > player.cols and not self.is_wall(self.rows, self.cols - 1, map):
                return LEFT
            else: # wall blocked target direction, rand instead.
                return self.random_direction(map)

    # The flee algorithm is in the opposite direction of chase. just return opposite direction under
    # The same circumstance. Note that there is no 50% odd to move randomly because the monster will
    # try to run as fast as possible.
    # The algorithm is not displayed in the game, since some technical issues.

    def flee(self, player, map):
        if self.rows < player.rows and not self.is_wall(self.rows + 1, self.cols, map):
            return UP
        elif self.rows > player.rows and not self.is_wall(self.rows - 1, self.cols, map):
            return DOWN
        elif self.cols < player.cols and not self.is_wall(self.rows, self.cols + 1, map):
            return LEFT
        elif self.cols > player.cols and not self.is_wall(self.rows, self.cols - 1, map):
            return RIGHT
        else:  # wall blocked target direction, rand instead.
            return self.random_direction(map)

    # The method returns a random movable (no wall ahead) direction

    def random_direction(self, map):
        dirs = randint(0, 3)
        while True:
            if dirs == UP and not self.is_wall(self.rows - 1, self.cols, map):
                return UP
            elif dirs == DOWN and not self.is_wall(self.rows + 1, self.cols, map):
                return DOWN
            elif dirs == LEFT and not self.is_wall(self.rows, self.cols - 1, map):
                return LEFT
            elif dirs == RIGHT and not self.is_wall(self.rows, self.cols + 1, map):
                return RIGHT
            else:
                dirs = randint(0, 3)

    # The algorithm directly move monster to target position.

    def just_move(self, map, dirs):

        if dirs == UP:
            Actor.move_up(self, map, 1)
            self.direction = UP
        elif dirs == DOWN:
            Actor.move_down(self, map, 1)
            self.direction = DOWN
        elif dirs == LEFT:
            Actor.move_left(self, map, 1)
            self.direction = LEFT
        else:
            Actor.move_right(self, map, 1)
            self.direction = RIGHT

    # The greater function that help the monster to make decision.

    def move(self, map, player):

        if not self.is_at_cross(map) and not self.is_at_corner(map):
            self.just_move(map, self.direction)
        elif self.is_at_corner(map):
            if self.is_wall(self.rows + 1, self.cols, map) and self.is_wall(self.rows , self.cols + 1, map):
                if randint(0,1) == 0:
                    self.just_move(map, LEFT)
                else:
                    self.just_move(map,UP)
            elif self.is_wall(self.rows + 1, self.cols, map) and self.is_wall(self.rows , self.cols - 1, map):
                if randint(0,1) == 0:
                    self.just_move(map, RIGHT)
                else:
                    self.just_move(map,UP)
            elif self.is_wall(self.rows - 1, self.cols, map) and self.is_wall(self.rows , self.cols + 1, map):
                if randint(0,1) == 0:
                    self.just_move(map, LEFT)
                else:
                    self.just_move(map, DOWN)
            elif self.is_wall(self.rows - 1, self.cols, map) and self.is_wall(self.rows, self.cols - 1, map):
                if randint(0,1) == 0:
                    self.just_move(map, RIGHT)
                else:
                    self.just_move(map, DOWN)

        else:
            # Fleeting is not implemented

            self.seek(player)
            if self.found_player:
                dirs = self.chase(player, map)
                self.just_move(map, dirs)
            else:
                dirs = self.random_direction(map)
                self.just_move(map, dirs)

    # if the monster catch player, the game ends.

    def catch_player(self, player):
        if self.rows == player.rows and self.cols == player.cols:
            return True
        return False

    # display the monsters in the pygame window. Red circle.

    def display(self, map):
        pygame.draw.circle(map.screen, BLUE, (self.cols * map.step + 10, self.rows * map.step + 10), 7)


if __name__ == "__main__":

    map = Maze()

    player = Player(map)
    monster1 = Monster(map)
    monster2 = Monster(map)
    clock = pygame.time.Clock()

    end = True
    while end:  # main game loop

        map.screen.fill(BLACK)
        map.on_draw_wall()
        player.display(map)
        monster1.display(map)
        monster2.display(map)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left(map, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right(map, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move_up(map, 0)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move_down(map, 0)

        monster1.move(map, player)
        if monster1.catch_player(player):
            print("you lose")
            end = False
        monster2.move(map, player)
        if monster2.catch_player(player):
            print("you lose")
            end = False

        clock.tick(10)
        pygame.display.flip()

    pygame.display.flip()

