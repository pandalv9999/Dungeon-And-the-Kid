import numpy as np

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
    size = [1000, 800]
    MAX_COL = 50
    MAX_ROW = 40

    def __init__(self, screen, levels):
        self.screen = screen
        self.levels = levels

    def display(self):

        for objects in self.object_list:
            objects.display()
        for monster in self.monster_list:
            monster.display()


########################################################################
#   The file of code defines the The room of the game                  #
########################################################################

# A room is defined with its Top_Left corner, its width and its height.

class Room:

    top_left_position = None
    width = 0
    height = 0
    is_connected = False

    def __init__(self, position, width, height):
        self.width = width
        self.height = height
        self.top_left_position = position




