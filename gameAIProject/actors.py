UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

########################################################################
#   The file of code defines the The actors of the game                #
########################################################################


class Actors:

    STR = 0
    DEF = 0
    INT = 0
    DEX = 0
    HP = 0
    MAX_HP = 0
    MP = 0
    MAX_MP = 0

    row = 0
    col = 0
    orientation = 0

    maze = None

    def __init__(self, maze, row, col):
        self.row = row
        self.col = col
        self.maze = maze

    def unchecked_move(self, direction):

        if direction == UP:
            self.row -= 1
        elif direction == DOWN:
            self.row += 1
        elif direction == LEFT:
            self.col -= 1
        elif direction == RIGHT:
            self.col += 1

    def is_wall_ahead(self, direction):

        if direction == UP and self.maze.is_wall(self.row - 1, self.col):
            return True
        elif direction == DOWN and self.maze.is_wall(self.row + 1, self.col):
            return True
        elif direction == LEFT and self.maze.is_wall(self.row, self.col - 1):
            return True
        elif direction == RIGHT and self.maze.is_wall(self.row, self.col + 1):
            return True
        return False


class Player(Actors):

    inventory = []
    armor = None
    weapon = None
    shield = None

    def __init__(self, maze, row=0, col=0):
        Actors.__init__(self, maze, row, col)

    def move(self, direction):
        if not self.is_wall_ahead(direction):
            self.unchecked_move(direction)