from random import randint
import math

# The global parameters of the screen

MAX_ROW = 0
MAX_COL = 0


def distance_to(sr, sc, tr, tc):

    return math.sqrt((tr - sr) * (tr - sr) + (tc - sc) * (tc - sc))


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
        return "Scroll of STR"

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
        self.owner.MAX_MP += 500 + 100 * randint(0, 5)


class ScrollsOfTeleportation(Scrolls):

    def __str__(self):
        return "Scroll of Teleportation"

    def use(self):
        # create randpos in the map, depending on the max_col and max_row, and whether there is walls.
        # To be implemented.
        randpos = 0
        self.owner.position = randpos


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


class HitPointPotion(Potions):

    def __str__(self):
        return "HP Potion"

    def use(self):

        self.owner.HP += self.owner.MAX_HP * 0.4
        if self.owner.HP > self.owner.MAX_HP:
            self.owner.HP = self.owner.MAX_HP


class HitPointSuperPotion(Potions):

    def __str__(self):
        return "HP Super Potion"

    def use(self):

        self.owner.HP = self.owner.MAX_HP


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
        self.owner.HP = self.owner.MAX_HP


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

    def attack(self):
        # Generate a bomb on the ground.
        return


class Armors(Objects):

    STR = 0
    DEF = 0
    INT = 0
    DEX = 0
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
        self.durability = 200
















