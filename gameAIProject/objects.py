from random import randint
import pygame
from gameAIProject import actors

# The global parameters of the screen

MAX_ROW = 0
MAX_COL = 0

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
#   The file of code defines the objects that would appeared in game.  #
########################################################################

# owner: the owner of the object. (If it is equipped by character, or picked up by character)
# position: the position of the object, if it is in the map.


class Objects:

    owner = None
    row = 0
    col = 0

    def __init__(self, row=0, col=0, owner=None):

        self.owner = owner
        self.row = row
        self.col = col


########################################################################
#   The block defines the scrolls in the game                          #
########################################################################

# __str__ creates string representation for each scrolls
# use() make effects to the owner of the scrolls.


class Scrolls(Objects):

    def display(self):

        # display the scrolls if it is in screen
        return

    def use(self):
        return


class ScrollsOfSTR(Scrolls):

    def __str__(self):
        return "Scroll of STR"

    def use(self):
        self.owner.STR += 5 + randint(0, 5)


class ScrollsOfDEF(Scrolls):

    def __str__(self):
        return "Scroll of DEF"

    def use(self):
        self.owner.DEF += 5 + randint(0, 5)


class ScrollsOfINT(Scrolls):

    def __str__(self):
        return "Scroll of INT"

    def use(self):
        self.owner.INT += 5 + randint(0, 5)


class ScrollsOfDEX(Scrolls):

    def __str__(self):
        return "Scroll of DEX"

    def use(self):
        self.owner.DEX += 5 + randint(0, 5)


class ScrollsOfHP(Scrolls):

    def __str__(self):
        return "Scroll of HP"

    def use(self):
        self.owner.MAX_HP += 500 + 100 * randint(0, 5)


class ScrollsOfMP(Scrolls):

    def __str__(self):
        return "Scroll of MP"

    def use(self):
        self.owner.MAX_MP += 20 + 2 * randint(0, 5)


class ScrollsOfTeleportation(Scrolls):

    def __str__(self):
        return "Scroll of Teleportation"

    def use(self):
        self.owner.maze.add_player_randomly(self.owner)


class ScrollsOfResurrection(Scrolls):

    def __str__(self):
        return "Scroll of Resurrection"

    def use(self):
        # resurrect the player when he is dead. To be implemented.
        return


########################################################################
#   The block defines the portion in the game                          #
########################################################################


# __str__ creates string representation for each scrolls
# use() make effects to the owner of the scrolls.

class Potions(Objects):

    def display(self):

        # display the scrolls if it is in screen
        return

    def use(self):
        return


class HitPointPotion(Potions):

    def __str__(self):
        return "HP Potion"

    def use(self):

        self.owner.HP += self.owner.total_max_hp() * 0.4
        if self.owner.HP > self.owner.total_max_hp():
            self.owner.HP = self.owner.total_max_hp()


class HitPointSuperPotion(Potions):

    def __str__(self):
        return "HP Super Potion"

    def use(self):

        self.owner.HP = self.owner.total_max_hp()


class MagicPointPotion(Potions):

    def __str__(self):
        return "MP Potion"

    def use(self):

        self.owner.MP += self.owner.MAX_MP * 0.4
        if self.owner.MP > self.owner.MAX_MP:
            self.owner.MP = self.owner.MAX_MP


class MagicPointSuperPotion(Potions):

    def __str__(self):
        return "MP Super Potion"

    def use(self):
        self.owner.MP = self.owner.MAX_MP


class Elixir(Potions):

    def __str__(self):
        return "Elixir"

    def use(self):

        self.owner.MP = self.owner.MAX_MP
        self.owner.HP = self.owner.total_max_hp()


########################################################################
#   The block defines the Weapons in the game                          #
########################################################################

# attack(target): attack the target by different means.
# Use dictionary to put the equipment to the player.


class Weapons(Objects):

    STR = 0
    DEF = 0
    INT = 0
    DEX = 0
    MAX_HP = 0
    durability = 0
    MAX_ATK_distance = 0


class MeleeWeapons(Weapons):

    def attack(self, target):
            # do the attack
        return


class ShortSword(MeleeWeapons):

    def __str__(self):
        return "Short Sword"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.STR = 5 + randint(0, 10)
        self.durability = 50


class LongSword(MeleeWeapons):

    def __str__(self):
        return "Long Sword"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.STR = 10 + randint(0, 15)
        self.durability = 100


class HeavySword(MeleeWeapons):

    def __str__(self):
        return "Heavy Sword"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.STR = 20 + randint(0, 30)
        self.DEF = 5 + randint(0, 10)
        self.DEX = -5 - randint(0, 10)
        self.durability = 200


class SorceryWeapons(Weapons):

    def attack(self, target):

            # generate a bullet
        return


class WoodStaff(SorceryWeapons):

    def __str__(self):
        return "Wood Staff"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.INT = 5 + randint(0, 10)
        self.DEF = 5 + randint(0, 10)
        self.durability = 100


class WindStaff(SorceryWeapons):

    def __str__(self):
        return "Wind Staff"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.INT = 5 + randint(0, 10)
        self.DEX = 5 + randint(0, 10)
        self.durability = 100


class WaterStaff(SorceryWeapons):

    def __str__(self):
        return "Water Staff"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.INT = 5 + randint(0, 10)
        self.MAX_HP = 500 + randint(0, 500)
        self.durability = 200


class FireStaff(SorceryWeapons):

    def __str__(self):
        return "Fire Staff"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.INT = 20 + randint(0, 30)
        self.DEF = -5 - randint(0, 10)
        self.durability = 50


class SleepFang(SorceryWeapons):

    def __str__(self):
        return "Sleep Fang"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.INT = 5 + randint(0, 10)
        self.durability = 50

    def attack(self, target):
        # Attack can make enemy sleep
        return


class AlchemyBomb(Weapons):

    def __str__(self):
        return "Alchemy Bomb"

    def attack(self):
        # Generate a bomb on the ground.
        return


class Armors(Objects):

    STR = 0
    DEF = 0
    INT = 0
    DEX = 0
    MAX_HP = 0
    durability = 0
    MAX_ATK_distance = 0

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)


class Robe(Armors):

    def __str__(self):
        return "Robe"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.DEF = 5 + randint(0, 10)
        self.INT = 5 + randint(0, 10)
        self.durability = 50


class ChainMail(Armors):

    def __str__(self):
        return "Chain mail"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.DEF = 10 + randint(0, 13)
        self.durability = 100


class Plate(Armors):

    def __str__(self):
        return "Plate"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.DEF = 20 + randint(0, 30)
        self.DEX = -5 - randint(0, 10)
        self.MAX_HP = 500 + randint(0, 500)
        self.durability = 200


class RoundShield(Armors):

    def __str__(self):
        return "Round Shield"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.DEF = 5 + randint(0, 10)
        self.STR = 5 + randint(0, 10)
        self.durability = 50


class TowerShield(Armors):

    def __str__(self):
        return "Tower Shield"

    def __init__(self, row=0, col=0, owner=None):
        Objects.__init__(self, row, col, owner)
        self.DEF = 20 + randint(0, 30)
        self.STR = 20 + randint(0, 30)
        self.DEX = -20 - randint(0, 30)
        self.MAX_HP = 1000 + randint(0, 500)
        self.durability = 200


########################################################################
#   The block defines the Sorcery in the game                          #
########################################################################

class Magic:

    def proceeds(self):
        return

    def display(self):
        return


class Sorcery(Magic):

    row = 0
    col = 0
    orientation = 0
    maze = None
    attacker = None
    defender = None
    step = 0

    def __init__(self, row, col, orientation, maze, attacker, defender=None):
        self.row = row
        self.col = col
        self.orientation = orientation
        self.maze = maze
        self.attacker = attacker
        self.defender = defender
        self.step = 10 + int(self.attacker.total_int() / 10)

    def proceeds(self):     # implement sleep later.
        next_row = 0
        next_col = 0
        if self.orientation == UP:
            next_col = self.col
            next_row = self.row - 1
        elif self.orientation == DOWN:
            next_col = self.col
            next_row = self.row + 1
        elif self.orientation == LEFT:
            next_col = self.col - 1
            next_row = self.row
        elif self.orientation == RIGHT:
            next_col = self.col + 1
            next_row = self.row

        if self.maze.is_wall(next_row, next_col) or self.step <= 0:
            self.maze.bullet_list.remove(self)
            del self
            return

        if self.defender is None:
            if self.maze.is_monster(next_row, next_col):
                self.defender = self.maze.monster_at(next_row, next_col)

        if self.defender is not None and next_row == self.defender.row and next_col == self.defender.col:

            damage = 10 + randint(0, max(0, self.attacker.total_int() - self.defender.total_int()))

            #   an sorcery attack does not take the durability of defender's armor.
            self.defender.HP -= damage
            if self.defender.HP <= 0:

                self.defender.HP = 0
                if isinstance(self.defender, actors.Monster):
                    self.attacker.EXP += self.defender.determine_basic_exp()
                    if self.attacker.EXP > self.attacker.get_max_exp():
                        self.attacker.EXP -= self.attacker.get_max_exp()
                        self.attacker.level_up()
                    self.defender.died()

            self.maze.bullet_list.remove(self)
            del self
            return

        self.row = next_row
        self.col = next_col
        self.step -= 1

    def display(self):
        image = get_image('sorcery.jpg')
        if self.orientation == DOWN:
            image = pygame.transform.rotate(image, -90)
        elif self.orientation == UP:
            image = pygame.transform.rotate(image, 90)
        elif self.orientation == LEFT:
            image = pygame.transform.flip(image, True, False)
        self.maze.screen.blit(image, (self.col * 20, self.row * 20), [0, 0, 20, 20])


class Meteorite(Magic):

    row = 0
    col = 0
    maze = None
    attacker = None
    defender = None
    step = 0

    def __init__(self, row, col, maze, attacker, defender):

        self.row = row
        self.col = col
        self.maze = maze
        self.attacker = attacker
        self.defender = defender
        self.step = 3

    def proceeds(self):

        self.row += 1
        self.col -= 1
        self.step -= 1

        if self.step == 0 or self.row == self.defender.row and self.col == self.defender.col:
            if self.row - 1 <= self.defender.row <= self.row + 1 and self.col - 1 <= self.defender.col <= self.col + 1:
                damage = 50 + 5 * randint(0, max(0, self.attacker.total_int() - self.defender.total_int()))
                self.defender.HP -= damage
                if self.defender.HP <= 0:
                    self.defender.HP = 0

            self.maze.bullet_list.remove(self)
            del self

    def display(self):
        image = get_image('metero.jpg')
        self.maze.screen.blit(image, (self.col * 20, self.row * 20), [0, 0, 20, 20])
















