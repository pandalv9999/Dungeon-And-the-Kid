from random import randint
from gameAIProject import objects, actors, PathFinding
import pygame

WHITE = (255, 255, 255)
BROWN = (90, 39, 41)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (238, 130, 238)

NULL = 0
WALL = 1
ARMORS = 6
WEAPONS = 7
POTION = 8
SCROLLS = 9
STAIR = 10

IMAGE_LIBRARY = {}


def get_image(path):
    global IMAGE_LIBRARY
    image = IMAGE_LIBRARY.get(path)
    if image is None:
        image = pygame.image.load(path)
        IMAGE_LIBRARY[path] = image
    return image


########################################################################
#   The file of code defines the The maze of the game                  #
########################################################################


class Maze:
    screen = None
    player = None
    path_finding = None
    levels = 0
    object_list = []
    monster_list = []
    room_list = []
    bullet_list = []
    maze = []
    size = [1300, 800]
    MAX_COL = 65
    MAX_ROW = 40
    step = 20
    stair_down_row = 0
    stair_down_col = 0

    def __init__(self, screen, levels):
        self.maze = []
        self.object_list = []
        self.monster_list = []
        self.bullet_list = []
        self.room_list = []
        self.player = None
        self.screen = None
        self.screen = screen
        self.levels = levels
        self.init_maze()
        self.add_objects()

    def __str__(self):
        return "The %d level of maze" % self.levels

    def init_maze(self):

        # Initialize the maze with all walls.

        for r in range(self.MAX_ROW):
            rows = []
            for c in range(self.MAX_COL):
                rows.append(WALL)
            self.maze.append(rows)

        # generate random Rooms

        number_rooms = randint(7, 9)

        for i in range(number_rooms):

            while True:

                is_occupied = False
                is_out_maze = False

                top_left_row = randint(1, self.MAX_ROW)
                top_left_col = randint(1, self.MAX_COL)
                width = randint(8, 15)
                height = randint(8, 15)

                for a in range(top_left_row - 1, min(self.MAX_ROW, (top_left_row + height + 1))):
                    for b in range(top_left_col - 1, min(self.MAX_COL, (top_left_col + width + 1))):
                        if a > self.MAX_ROW or b > self.MAX_COL or self.maze[a][b] == NULL:
                            is_occupied = True

                if top_left_row + height + 1 > self.MAX_ROW or top_left_col + width + 1 > self.MAX_COL:
                    is_out_maze = True

                if not is_out_maze and not is_occupied:
                    break

            room = Room(top_left_row, top_left_col, width, height)
            self.room_list.append(room)

            for a in range(top_left_row, top_left_row + height):
                for b in range(top_left_col, top_left_col + width):
                    self.maze[a][b] = NULL

        # sort the room to make it neat

        self.room_list.sort(key=lambda x: x.top_left_cols)

        # generate corridor between rooms

        for i in range(len(self.room_list) - 1):
            room_1 = self.room_list[i]
            room_2 = self.room_list[i + 1]

            if not room_1.connected or not room_2.connected:
                self.generate_path(room_1, room_2)

        # add stairs to the map.

        end_room = self.room_list[number_rooms - 1]
        self.stair_down_row = end_room.top_left_rows + randint(3, end_room.height - 3)
        self.stair_down_col = end_room.top_left_cols + randint(3, end_room.width - 3)
        self.maze[self.stair_down_row][self.stair_down_col] = STAIR

        self.path_finding = PathFinding(self.maze)

    # add objects to the map. Objects are stored in the map as numbers.

    def add_objects(self):

        num_objects = 7 + randint(0, 7)

        for i in range(0, num_objects):

            types = randint(0, 5)

            while True:
                rows = randint(0, self.MAX_ROW - 1)
                cols = randint(0, self.MAX_COL - 1)
                if self.maze[rows][cols] == NULL:
                    break

            if types == 0 or types == 1 or types == 2:  # potion

                subtypes = randint(0, 31)
                if subtypes in range(0, 10):
                    new_object = objects.HitPointPotion(rows, cols)
                elif subtypes in range(10, 20):
                    new_object = objects.MagicPointPotion(rows, cols)
                elif subtypes in range(20, 25):
                    new_object = objects.HitPointSuperPotion(rows, cols)
                elif subtypes in range(25, 30):
                    new_object = objects.MagicPointSuperPotion(rows, cols)
                else:
                    new_object = objects.Elixir(rows, cols)

                self.maze[rows][cols] = POTION

            elif types == 3:  # scrolls

                subtypes = randint(0, 7)
                if subtypes == 0:
                    new_object = objects.ScrollsOfDEF(rows, cols)
                elif subtypes == 1:
                    new_object = objects.ScrollsOfDEX(rows, cols)
                elif subtypes == 2:
                    new_object = objects.ScrollsOfHP(rows, cols)
                elif subtypes == 3:
                    new_object = objects.ScrollsOfINT(rows, cols)
                elif subtypes == 4:
                    new_object = objects.ScrollsOfMP(rows, cols)
                elif subtypes == 5:
                    new_object = objects.ScrollsOfSTR(rows, cols)
                elif subtypes == 6:
                    new_object = objects.ScrollsOfTeleportation(rows, cols)
                else:
                    new_object = objects.ScrollsOfResurrection(rows, cols)

                self.maze[rows][cols] = SCROLLS

            elif types == 4:  # weapon

                subtypes = randint(0, 9)
                if subtypes == 0:
                    new_object = objects.ShortSword(rows, cols)
                elif subtypes == 1:
                    new_object = objects.LongSword(rows, cols)
                elif subtypes == 2:
                    new_object = objects.HeavySword(rows, cols)
                elif subtypes == 3:
                    new_object = objects.WoodStaff(rows, cols)
                elif subtypes == 4:
                    new_object = objects.WindStaff(rows, cols)
                elif subtypes == 5:
                    new_object = objects.WaterStaff(rows, cols)
                elif subtypes == 6:
                    new_object = objects.FireStaff(rows, cols)
                elif subtypes == 7:
                    new_object = objects.SleepFang(rows, cols)
                else:
                    new_object = objects.AlchemyBomb(rows, cols)

                self.maze[rows][cols] = WEAPONS

            else:  # armor
                subtypes = randint(0, 9)
                if subtypes in range(0, 3):
                    new_object = objects.Robe(rows, cols)
                elif subtypes in range(3, 6):
                    new_object = objects.ChainMail(rows, cols)
                elif subtypes == 6:
                    new_object = objects.Plate(rows, cols)
                elif subtypes == 7 or subtypes == 8:
                    new_object = objects.RoundShield(rows, cols)
                else:
                    new_object = objects.TowerShield(rows, cols)

                self.maze[rows][cols] = ARMORS

            self.object_list.append(new_object)

    # add monsters to the map.

    def add_monsters(self):

        # tentative implementation. add a goblin.

        num_monster = 5 + randint(self.levels, 5)
        for i in range(num_monster):
            start_room = self.room_list[0]

            while True:
                row = randint(0, self.MAX_ROW - 1)
                col = randint(0, self.MAX_COL - 1)
                if row not in range(start_room.top_left_rows, start_room.top_left_rows + start_room.height) \
                        and col not in range(start_room.top_left_cols, start_room.top_left_cols + start_room.width) \
                        and self.maze[row][col] == NULL:
                    break

            #   right now only have goblins

            if self.levels <= 2:
                monster = actors.Goblin(self, row, col, randint(self.levels + 1, self.levels + 3), self.player)
            elif self.levels <= 5:
                if randint(0, 1) == 1:
                    monster = actors.Goblin(self, row, col, randint(self.levels + 1, self.levels + 3), self.player)
                else:
                    monster = actors.DarkWitches(self, row, col, randint(self.levels + 1, self.levels + 3), self.player)
            self.monster_list.append(monster)

    # put the player to the map

    def add_player(self, player):

        start_room = self.room_list[0]

        while True:
            row = start_room.top_left_rows + randint(1, start_room.height - 1)
            col = start_room.top_left_cols + randint(1, start_room.width - 1)
            if self.maze[row][col] == NULL:
                break

        player.row = row
        player.col = col
        self.player = player

    # put the player in the map at random position

    def add_player_randomly(self, player):

        self.player = None
        while True:
            row = randint(0, self.MAX_ROW)
            col = randint(0, self.MAX_COL)
            if self.maze[row][col] == NULL:
                break

        player.row = row
        player.col = col
        self.player = player

    # given a row number and col number, return if it is a wall.

    def is_wall(self, row, col):

        return self.maze[row][col] == WALL

    # given a row number and col number, return if it is a wall.

    def is_stair(self, row, col):

        return self.stair_down_col == col and self.stair_down_row == row

    # give a row number and col number, return if it is a object.

    def is_object(self, row, col):

        return self.maze[row][col] in range(6, 10)

    # given a row number and col number, return the object at that position, or None if there is no object.

    def object_at(self, row, col):

        for objects in self.object_list:
            if objects.row == row and objects.col == col:
                return objects
        return None

    # remove a particular object

    def remove_object(self, objects):
        self.object_list.remove(objects)
        self.maze[objects.row][objects.col] = NULL

    # give a row number and col number, return true if it is a monster.

    def is_monster(self, row, col):
        for monsters in self.monster_list:
            if monsters.row == row and monsters.col == col:
                return True
        return False

    # give a row number and col number, return the monster at that position.

    def monster_at(self, row, col):
        for monsters in self.monster_list:
            if monsters.row == row and monsters.col == col:
                return monsters
        return None

    # display the content on the map.

    def display(self):

        # Stationary Objects

        for i in range(self.MAX_ROW):
            for j in range(self.MAX_COL):
                if self.maze[i][j] == WALL:
                    image = get_image('wall.jpg')
                    self.screen.blit(image, (j * self.step, i * self.step), [0, 0, self.step, self.step])
                elif self.maze[i][j] == STAIR:
                    image = get_image('stair.jpg')
                    self.screen.blit(image, (j * self.step, i * self.step), [0, 0, self.step, self.step])
                elif self.maze[i][j] == SCROLLS:
                    image = get_image('scroll.jpg')
                    self.screen.blit(image, (j * self.step, i * self.step), [0, 0, self.step, self.step])
                elif self.maze[i][j] == POTION:
                    image = get_image('potion.jpg')
                    self.screen.blit(image, (j * self.step, i * self.step), [0, 0, self.step, self.step])
                elif self.maze[i][j] == ARMORS:
                    image = get_image('shield.jpg')
                    self.screen.blit(image, (j * self.step, i * self.step), [0, 0, self.step, self.step])
                elif self.maze[i][j] == WEAPONS:
                    image = get_image('weapon.jpg')
                    self.screen.blit(image, (j * self.step, i * self.step), [0, 0, self.step, self.step])

        # Moving characters

        self.player.display()
        for bullet in self.bullet_list:
            bullet.display()
        for monsters in self.monster_list:
            monsters.display()

    # generate a path between room

    def generate_path(self, room_1, room_2):

        room_1_row = room_1.top_left_rows + randint(2, room_1.height - 2)
        room_1_col = room_1.top_left_cols + randint(2, room_1.width - 2)
        room_2_row = room_2.top_left_rows + randint(2, room_2.height - 2)
        room_2_col = room_2.top_left_cols + randint(2, room_2.width - 2)
        self.connect(room_1_row, room_1_col, room_2_row, room_2_col, randint(0, 1))
        room_1.connected = True
        room_2.connected = True

    # helper function to generate path(recursive)

    def connect(self, sr, sc, tr, tc, pattern):

        if pattern == 1:
            if sr > tr:
                self.connect(sr - 1, sc, tr, tc, pattern)
            elif sr < tr:
                self.connect(sr + 1, sc, tr, tc, pattern)
            elif sc > tc:
                self.connect(sr, sc - 1, tr, tc, pattern)
            elif sc < tc:
                self.connect(sr, sc + 1, tr, tc, pattern)
            else:
                return
        else:
            if sc > tc:
                self.connect(sr, sc - 1, tr, tc, pattern)
            elif sc < tc:
                self.connect(sr, sc + 1, tr, tc, pattern)
            elif sr > tr:
                self.connect(sr - 1, sc, tr, tc, pattern)
            elif sr < tr:
                self.connect(sr + 1, sc, tr, tc, pattern)
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
    connected = False

    def __init__(self, rows, cols, width, height):
        self.width = width
        self.height = height
        self.top_left_rows = rows
        self.top_left_cols = cols
