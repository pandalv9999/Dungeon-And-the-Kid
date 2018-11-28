from random import randint
import pygame

WHITE = (255, 255, 255)
BROWN = (90, 39, 41)

########################################################################
#   The file of code defines the The maze of the game                  #
########################################################################


class Maze:

    screen = None
    levels = 0
    object_list = []
    monster_list = []
    room_list = []
    maze = []
    size = [1300, 800]
    MAX_COL = 65
    MAX_ROW = 40
    step = 20
    stair_up = None
    stair_down = None

    def __init__(self, screen, levels):
        self.screen = screen
        self.levels = levels
        self.init_maze()
        self.add_objects()
        self.add_monsters()

    def __str__(self):
        return "The %d level of maze" % self.levels

    def init_maze(self):

        # Initialize the maze with all walls.

        for r in range(self.MAX_ROW):
            rows = []
            for c in range(self.MAX_COL):
                rows.append(1)
            self.maze.append(rows)

        print(len(self.maze))
        print(len(self.maze[0]))

        # generate random Rooms

        number_rooms = randint(4, 6)

        for i in range(number_rooms):

            while True:

                is_occupied = False
                is_out_maze = False

                top_left_row = randint(1, self.MAX_ROW)
                top_left_col = randint(1, self.MAX_COL)
                width = randint(16, 30)
                height = randint(8, 20)

                for a in range(top_left_row - 1, min(self.MAX_ROW, (top_left_row + height + 1))):
                    for b in range(top_left_col - 1, min(self.MAX_COL, (top_left_col + width + 1))):
                        if a > self.MAX_ROW or b > self.MAX_COL or self.maze[a][b] == 0:
                            is_occupied = True

                if top_left_row + height + 1 > self.MAX_ROW or top_left_col + width + 1 > self.MAX_COL:
                    is_out_maze = True

                if not is_out_maze and not is_occupied:
                    break

            room = Room(top_left_row, top_left_col, width, height)
            self.room_list.append(room)

            for a in range(top_left_row, top_left_row + height):
                for b in range(top_left_col, top_left_col + width):
                    self.maze[a][b] = 0

        # generate corridor between rooms

        for i in range(len(self.room_list) - 1):
            self.generate_path(self.room_list[i], self.room_list[i+1])

        # add stairs to the map.

    # add objects to the map

    def add_objects(self):
        return

    # add monsters to the map.

    def add_monsters(self):
        return

    # given a row number and col number, return if it is a wall.

    def is_wall(self, row, col):

        if self.maze[row][col] == 1:
            return True
        else:
            return False

    # given a row number and col number, return the object at that position, or None if there is no pbject.

    def object_at(self, row, col):

        for objects in self.object_list:
            if objects.row == row and objects.col == col:
                return objects

        return None

    # display the content on the map.

    def display(self):

        for i in range(self.MAX_ROW):
            for j in range(self.MAX_COL):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, BROWN, [j*self.step, i*self.step, self.step, self.step])

    # generate a path between room

    def generate_path(self, room_1, room_2):

        room_1_row = room_1.top_left_rows + randint(2, room_1.height - 2)
        room_1_col = room_1.top_left_cols + randint(2, room_1.width - 2)
        room_2_row = room_2.top_left_rows + randint(2, room_2.height - 2)
        room_2_col = room_2.top_left_cols + randint(2, room_2.width - 2)
        self.connect(room_1_row, room_1_col, room_2_row, room_2_col)

    # helper function to generate path(recursive)

    def connect(self, sr, sc, tr, tc):

        if sr > tr:
            self.connect(sr - 1, sc, tr, tc)
        elif sr < tr:
            self.connect(sr + 1, sc, tr, tc)
        elif sc > tc:
            self.connect(sr, sc - 1, tr, tc)
        elif sc < tc:
            self.connect(sr, sc + 1, tr, tc)
        else:
            return

        self.maze[sr][sc] = 0


########################################################################
#   The file of code defines the The room of the game                  #
########################################################################

# A room is defined with its Top_Left corner, its width and its height.


class Room:

    top_left_rows = 0
    top_left_cols = 0
    width = 0
    height = 0

    def __init__(self, rows, cols, width, height):
        self.width = width
        self.height = height
        self.top_left_rows = rows
        self.top_left_cols = cols




