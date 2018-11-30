from gameAIProject import objects
import pygame

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (238, 130, 238)

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


IMAGE_LIBRARY = {}


def get_image(path):
    global IMAGE_LIBRARY
    image = IMAGE_LIBRARY.get(path)
    if image is None:
        image = pygame.image.load(path)
        IMAGE_LIBRARY[path] = image
    return image

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
    level = 0

    row = 0
    col = 0
    orientation = 0

    armor = None
    weapon = None
    shield = None

    maze = None

    def __init__(self, maze, row, col):
        self.row = row
        self.col = col
        self.maze = maze

    def unchecked_move(self, direction):

        self.orientation = direction
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

    def total_str(self):

        total_STR = self.STR
        if self.weapon is not None:
            total_STR += self.weapon.STR
        if self.shield is not None:
            total_STR += self.shield.STR
        if self.armor is not None:
            total_STR += self.armor.STR
        return total_STR

    def total_def(self):

        total_DEF = self.DEF
        if self.weapon is not None:
            total_DEF += self.weapon.DEF
        if self.shield is not None:
            total_DEF += self.shield.DEF
        if self.armor is not None:
            total_DEF += self.armor.DEF
        return total_DEF

    def total_int(self):

        total_INT = self.INT
        if self.weapon is not None:
            total_INT += self.weapon.INT
        if self.shield is not None:
            total_INT += self.shield.INT
        if self.armor is not None:
            total_INT += self.armor.INT
        return total_INT

    def total_dex(self):

        total_DEX = self.DEX
        if self.weapon is not None:
            total_DEX += self.weapon.DEX
        if self.shield is not None:
            total_DEX += self.shield.DEX
        if self.armor is not None:
            total_DEX += self.armor.DEX
        return total_DEX

    def total_max_hp(self):
        total_MAX_HP = self.MAX_HP
        if self.weapon is not None:
            total_MAX_HP += self.weapon.MAX_HP
        if self.shield is not None:
            total_MAX_HP += self.shield.MAX_HP
        if self.armor is not None:
            total_MAX_HP += self.armor.MAX_HP
        return total_MAX_HP


class Player(Actors):

    EXP = 0
    inventory = []

    def __init__(self, maze, row=0, col=0):
        Actors.__init__(self, maze, row, col)
        self.level = 1
        self.MAX_HP = 500
        self.HP = 500
        self.MAX_MP = 100
        self.MP = 100
        self.weapon = objects.ShortSword(0, 0, self)

    def move(self, direction):
        if not self.is_wall_ahead(direction):
            self.unchecked_move(direction)

    def pick_up(self):

        if len(self.inventory) > 20:    # max inventory is 20
            return

        if self.maze.is_object(self.row, self.col):
            objects = self.maze.object_at(self.row, self.col)
            objects.owner = self
            self.inventory.append(objects)
            self.maze.remove_object(objects)

    def get_max_exp(self):
        return self.level * 100 + (self.level - 1) * (self.level - 1) * 10

    def display(self):

        image = get_image('kid.jpg')
        if self.orientation == DOWN:
            image = pygame.transform.rotate(image, -90)
        elif self.orientation == UP:
            image = pygame.transform.rotate(image, 90)
        elif self.orientation == LEFT:
            image = pygame.transform.flip(image, True, False)
        self.maze.screen.blit(image, (self.col * 20, self.row * 20), [0, 0, 20, 20])

        pygame.draw.rect(self.maze.screen, RED, [self.col * 20 - 15, self.row * 20 - 14, 50, 5])
        pygame.draw.rect(self.maze.screen, GREEN,
                         [self.col * 20 - 15, self.row * 20 - 14, 50 * (self.HP / self.MAX_HP), 5])
        pygame.draw.rect(self.maze.screen, RED, [self.col * 20 - 15, self.row * 20 - 9, 50, 5])
        pygame.draw.rect(self.maze.screen, BLUE,
                         [self.col * 20 - 15, self.row * 20 - 9, 50 * (self.MP / self.MAX_MP), 5])
