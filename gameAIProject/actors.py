from gameAIProject import objects, PathFinding
import pygame
import math
from random import randint

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (238, 130, 238)

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

MAX_COL = 65
MAX_ROW = 40


IMAGE_LIBRARY = {}


def get_image(path):
    global IMAGE_LIBRARY
    image = IMAGE_LIBRARY.get(path)
    if image is None:
        image = pygame.image.load(path)
        IMAGE_LIBRARY[path] = image
    return image


def distance_to(sr, sc, tr, tc):
    return math.sqrt((tr - sr) * (tr - sr) + (tc - sc) * (tc - sc))


########################################################################
#   The file of code defines the The FSM of actors in the game         #
########################################################################

State = type("State", (object,), {})


class Idle(object):

    monster = None

    def __init__(self, monster):
        self.monster = monster

    def execute(self):
        self.monster.idle()


class Wander(object):

    monster = None

    def __init__(self, monster):
        self.monster = monster

    def execute(self):
        self.monster.wander()


class Approach(object):

    monster = None

    def __init__(self, monster):
        self.monster = monster

    def execute(self):
        self.monster.path_seeking()


class Attack(object):

    monster = None

    def __init__(self, monster):
        self.monster = monster

    def execute(self):
        if isinstance(self.monster, Goblin):
            if self.monster.is_player_nearby():
                self.monster.melee_attack()
            else:
                self.monster.path_seeking()
        elif isinstance(self.monster, DarkWitches):
            self.monster.attack()


class Flee(object):

    monster = None

    def __init__(self, monster):
        self.monster = monster

    def execute(self):
        self.monster.flee()


class Transition(object):

    to_state = None

    def __init__(self, to_state):

        self.to_state = to_state


class FSM(object):

    def __init__(self, character):

        self.character = character
        self.states = {}
        self.transitions = {}
        self.current_state = None
        self.currentTransition = None

    def set_state(self, state_name):
        self.current_state = self.states[state_name]

    def transition(self, transition_name):
        self.currentTransition = self.transitions[transition_name]

    def execute(self):

        if self.currentTransition:

            self.set_state(self.currentTransition.to_state)
            self.currentTransition = None

        self.current_state.execute()


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
    orientation = 1

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

    def idle(self):
        return

    def wander(self):
        direction = randint(1, 4)
        if not self.is_wall_ahead(direction):
            self.unchecked_move(direction)

########################################################################
#   The file of code defines the The player of the game                #
########################################################################


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
        self.DEX = 10
        self.DEF = 10
        self.INT = 10
        self.STR = 10
        self.weapon = objects.ShortSword(0, 0, self)
        # self.weapon = objects.FireStaff(0, 0, self)

    def is_monster_ahead(self, direction):
        if direction == UP and self.maze.is_monster(self.row - 1, self.col):
            return True
        elif direction == DOWN and self.maze.is_monster(self.row + 1, self.col):
            return True
        elif direction == LEFT and self.maze.is_monster(self.row, self.col - 1):
            return True
        elif direction == RIGHT and self.maze.is_monster(self.row, self.col + 1):
            return True
        return False

    def move(self, direction):
        if not self.is_wall_ahead(direction) and not self.is_monster_ahead(direction):
            self.unchecked_move(direction)

    def pick_up(self):

        if len(self.inventory) > 20:    # max inventory is 20
            return

        if self.maze.is_object(self.row, self.col):
            objects = self.maze.object_at(self.row, self.col)
            objects.owner = self
            self.inventory.append(objects)
            self.maze.remove_object(objects)

    def melee_attack(self):
        monster = None
        if self.maze.is_monster(self.row, self.col + 1):
            monster = self.maze.monster_at(self.row, self.col + 1)
            self.orientation = RIGHT
        elif self.maze.is_monster(self.row, self.col - 1):
            monster = self.maze.monster_at(self.row, self.col - 1)
            self.orientation = LEFT
        elif self.maze.is_monster(self.row + 1, self.col):
            monster = self.maze.monster_at(self.row + 1, self.col)
            self.orientation = DOWN
        elif self.maze.is_monster(self.row - 1, self.col):
            monster = self.maze.monster_at(self.row - 1, self.col)
            self.orientation = UP

        if monster is not None:
            damage = 5 + randint(0, max(self.total_str() - monster.total_def(), 0))
            monster.HP -= damage
            if randint(0, 3) == 3 and self.weapon is not None:
                self.weapon.durability -= 1
                if self.weapon.durability <= 0:
                    self.weapon = None
            if randint(0, 3) == 3 and monster.armor is not None:
                monster.armor.durability -= 1
                if monster.armor.durability <= 0:
                    monster.armor = None
            if randint(0, 3) == 3 and monster.shield is not None:
                monster.shield.durability -= 1
                if monster.shield.durability <= 0:
                    monster.shield = None
            if monster.HP < 0:
                self.EXP += monster.determine_basic_exp()
                if self.EXP > self.get_max_exp():
                    self.EXP -= self.get_max_exp()
                    self.level_up()
                monster.died()

    def sorcery_attack(self):
        if not isinstance(self.weapon, objects.SorceryWeapons) or self.MP < 10:
            return

        self.MP -= 10
        sorcery = objects.Sorcery(self.row, self.col, self.orientation, self.maze, self)
        self.maze.bullet_list.append(sorcery)
        if randint(0, 3) == 0:
            self.weapon.durability -= 1
            if self.weapon.durability <= 0:
                self.weapon = None

    def get_max_exp(self):
        return self.level * 100 + (self.level - 1) * (self.level - 1) * 10

    def level_up(self):
        self.level += 1
        self.MAX_HP += randint(1, 5) * 50
        self.HP = self.total_max_hp()
        self.MP = self.MAX_MP
        self.STR += 5 + randint(0, 5)
        self.INT += 5 + randint(0, 5)
        self.DEX += 5 + randint(0, 5)
        self.DEF += 5 + randint(0, 5)

    def cheat(self):
        self.STR = 999
        self.INT = 999
        self.DEX = 999
        self.DEF = 999
        self.MAX_HP = 99999
        self.MAX_MP = 999

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
                         [self.col * 20 - 15, self.row * 20 - 14, 50 * (self.HP / self.total_max_hp()), 5])
        pygame.draw.rect(self.maze.screen, RED, [self.col * 20 - 15, self.row * 20 - 9, 50, 5])
        pygame.draw.rect(self.maze.screen, BLUE,
                         [self.col * 20 - 15, self.row * 20 - 9, 50 * (self.MP / self.MAX_MP), 5])


########################################################################
#   The file of code defines the The monster of the game               #
########################################################################

# Monster is initialized after the player is added to the map.

class Monster(Actors):

    player = None
    fsm = None
    last_path_finding = 0
    last_movement = 0
    path = []
    flee_path = []
    current_step = 0
    PATH_FINDING_INTERVAL = 3000  # 5 sec
    MOVEMENT_THRESHOLD = 200      # 200 - DEX
    path_finding = None

    def determine_basic_attr(self):
        return self.level + 5 * randint(self.level - 1, self.level + 3)

    def determine_basic_exp(self):
        return self.level * 50 + 10 * randint(0, self.level)

    def path_seeking(self):

        if self.current_step >= len(self.path):
            # self.path_finding.setStartEnd(self.row, self.col, self.player.row, self.player.col)
            # self.path = self.path_finding.aStar()
            self.path = self.path_finding.dijkstra(self.row, self.col, self.player.row, self.player.col)
            self.current_step = 0
            self.last_path_finding = pygame.time.get_ticks()

        next_move = self.path[self.current_step]
        next_move_row = next_move[0]
        next_move_col = next_move[1]
        if next_move_row == self.row and next_move_col == self.col + 1:
            self.unchecked_move(RIGHT)
        elif next_move_row == self.row and next_move_col == self.col - 1:
            self.unchecked_move(LEFT)
        elif next_move_col == self.col and next_move_row == self.row + 1:
            self.unchecked_move(DOWN)
        elif next_move_col == self.col and next_move_row == self.row - 1:
            self.unchecked_move(UP)
        self.current_step += 1

    def is_player_nearby(self):
        if self.player.row == self.row and (self.player.col - 1 == self.col or self.player.col + 1 == self.col):
            return True
        if self.player.col == self.col and (self.player.row - 1 == self.row or self.player.row + 1 == self.row):
            return True
        return False

    def melee_attack(self):
        damage = 5 + randint(0, max(self.total_str() - self.player.total_def(), 0))
        self.player.HP -= damage
        if randint(0, 3) == 3 and self.weapon is not None:
            self.weapon.durability -= 1
            if self.weapon.durability <= 0:
                self.weapon = None
        if randint(0, 3) == 3 and self.player.armor is not None:
            self.player.armor.durability -= 1
            if self.player.armor.durability <= 0:
                self.player.armor = None
        if randint(0, 3) == 3 and self.player.shield is not None:
            self.player.shield.durability -= 1
            if self.player.shield.durability <= 0:
                self.player.shield = None
        if self.player.HP < 0:
            self.player.HP = 0

    def died(self):
        return

    def flee(self):

        if len(self.flee_path) <= 0:
            end_room = self.maze.room_list[-1]
            row = end_room.top_left_rows + randint(3, end_room.height - 3)
            col = end_room.top_left_cols + randint(3, end_room.width - 3)
            # self.path_finding.setStartEnd(self.row, self.col, row, col)
            # self.flee_path = self.path_finding.aStar()
            self.flee_path = self.path_finding.dijkstra(self.row, self.col, row, col)
            self.current_step = 0

        if self.current_step >= len(self.flee_path):
            return

        next_move = self.flee_path[self.current_step]
        next_move_row = next_move[0]
        next_move_col = next_move[1]
        if next_move_row == self.row and next_move_col == self.col + 1:
            self.unchecked_move(RIGHT)
        elif next_move_row == self.row and next_move_col == self.col - 1:
            self.unchecked_move(LEFT)
        elif next_move_col == self.col and next_move_row == self.row + 1:
            self.unchecked_move(DOWN)
        elif next_move_col == self.col and next_move_row == self.row - 1:
            self.unchecked_move(UP)
        self.current_step += 1


class Goblin(Monster):

    idling = True
    wandering = False
    seeking = False
    attacking = False
    fleeing = False

    awake_time = 0
    smelling_distance = 0
    LARGEST_AWAKE_TIME = 10000      # 10 sec

    def __init__(self, maze, row, col, level, player):
        Actors.__init__(self, maze, row, col)
        self.level = level
        self.player = player
        self.smelling_distance = 20 + self.level * 2
        self.INT = self.determine_basic_attr()
        self.STR = self.determine_basic_attr()
        self.DEF = self.determine_basic_attr()
        self.DEX = 5 * self.determine_basic_attr()
        self.MAX_HP = 100 + self.level * randint(0, 100)
        self.HP = self.MAX_HP
        self.weapon = objects.ShortSword(0, 0, self)
        self.init_fsm()
        self.path_finding = None
        self.path_finding = PathFinding.PathFinding(self.maze.maze)

    def init_fsm(self):
        self.fsm = FSM(self)
        self.fsm.states["Idle"] = Idle(self)
        self.fsm.states["Wander"] = Wander(self)
        self.fsm.states["Approach"] = Approach(self)
        self.fsm.states["Attack"] = Attack(self)
        self.fsm.states["Flee"] = Flee(self)

        self.fsm.transitions["IdleToWander"] = Transition("Wander")
        self.fsm.transitions["WanderToIdle"] = Transition("Idle")
        self.fsm.transitions["WanderToApproach"] = Transition("Approach")
        self.fsm.transitions["ApproachToAttack"] = Transition("Attack")
        self.fsm.transitions["ApproachToIdle"] = Transition("Idle")
        self.fsm.transitions["AttackToWander"] = Transition("Wander")
        self.fsm.transitions["AttackToFlee"] = Transition("Flee")
        self.fsm.transitions["FleeToWander"] = Transition("Wander")

        self.fsm.set_state("Idle")

    def change_state(self):

        print(self.row, self.col)
        print(self.maze.maze)

        now = pygame.time.get_ticks()

        if now - self.last_movement < self.MOVEMENT_THRESHOLD - self.DEX:
            return

        if self.path == [] or now - self.last_path_finding > self.PATH_FINDING_INTERVAL:
            # self.path_finding.setStartEnd(self.row, self.col, self.player.row, self.player.col)
            # self.path = self.path_finding.aStar()
            self.path = self.path_finding.dijkstra(self.row, self.col, self.player.row, self.player.col)
            self.current_step = 0
            self.last_path_finding = now

        if self.idling:
            self.HP += 2
            if self.HP > self.total_max_hp():
                self.HP = self.total_max_hp()
            if distance_to(self.row, self.col, self.player.row, self.player.col) < self.smelling_distance:
                # Add global alerting later
                self.fsm.transition("IdleToWander")
                self.idling = False
                self.wandering = True
                self.seeking = False
                self.attacking = False
                self.fleeing = False
                self.awake_time = now

        if self.wandering:
            self.HP += 2
            if self.HP > self.total_max_hp():
                self.HP = self.total_max_hp()
            if len(self.path) < 30:     # considering alerting later.
                self.fsm.transition("WanderToApproach")
                self.awake_time = now
                self.idling = False
                self.wandering = False
                self.seeking = True
                self.attacking = False
                self.fleeing = False

            if now - self.awake_time > self.LARGEST_AWAKE_TIME:
                self.fsm.transition("WanderToIdle")     # is this good? not sure
                self.idling = True
                self.wandering = False
                self.seeking = False
                self.attacking = False
                self.fleeing = False

        if self.seeking:
            if distance_to(self.row, self.col, self.player.row, self.player.col) < 5:
                self.fsm.transition("ApproachToAttack")
                self.idling = False
                self.wandering = False
                self.seeking = False
                self.attacking = True
                self.fleeing = False
                self.awake_time = now

            if now - self.awake_time > self.LARGEST_AWAKE_TIME:
                self.fsm.transition("ApproachToIdle")
                self.idling = True
                self.wandering = False
                self.seeking = False
                self.attacking = False
                self.fleeing = False

        if self.attacking:
            if self.HP < self.MAX_HP / 4 and randint(0, 3) == 0:
                self.fsm.transition("AttackToFlee")
                self.idling = False
                self.wandering = False
                self.seeking = False
                self.attacking = False
                self.fleeing = True
                self.awake_time = now

        if self.fleeing:
            if distance_to(self.row, self.col, self.player.row, self.player.col) > 20:      # consider revise
                self.fsm.transition("FleeToWander")
                self.awake_time = now
                self.idling = False
                self.wandering = True
                self.seeking = False
                self.attacking = False
                self.fleeing = False
                self.awake_time = now

        self.fsm.execute()
        self.last_movement = now

    def died(self):
        dropped = None
        odd = randint(0, 3)
        if odd == 0:
            dropped = objects.HitPointPotion(self.row, self.col)
        elif odd == 1:
            dropped = objects.MagicPointPotion(self.row, self.col)

        if dropped is not None:
            self.maze.object_list.append(dropped)
            self.maze.maze[self.row][self.col] = 8
        self.maze.monster_list.remove(self)

    def display(self):
        image = get_image('goblin.jpg')
        image = pygame.transform.flip(image, True, False)
        if self.orientation == DOWN:
            image = pygame.transform.rotate(image, -90)
        elif self.orientation == UP:
            image = pygame.transform.rotate(image, 90)
        elif self.orientation == LEFT:
            image = pygame.transform.flip(image, True, False)
        self.maze.screen.blit(image, (self.col * 20, self.row * 20), [0, 0, 20, 20])

        pygame.draw.rect(self.maze.screen, RED, [self.col * 20 - 15, self.row * 20 - 9, 50, 5])
        pygame.draw.rect(self.maze.screen, GREEN,
                         [self.col * 20 - 15, self.row * 20 - 9, 50 * (self.HP / self.MAX_HP), 5])


class DarkWitches(Monster):

    idling = True
    seeking = False
    attacking = False
    fleeing = False

    smelling_distance = 0
    awake_time = 0
    LARGEST_AWAKE_TIME = 5000  # 10 sec
    last_telescope = 0
    TELESCOPE_INTERVAL = 3000

    def __init__(self, maze, row, col, level, player):
        Actors.__init__(self, maze, row, col)
        self.level = level
        self.player = player
        self.INT = 2 * self.determine_basic_attr()
        self.STR = self.determine_basic_attr()
        self.DEF = 2 * self.determine_basic_attr()
        self.DEX = 2 * self.determine_basic_attr()
        self.MAX_HP = 80 + self.level * randint(0, 100) * 0.8
        self.HP = self.MAX_HP
        self.MAX_MP = 200
        self.MP = 200
        self.armor = objects.Robe(0, 0, self)
        self.weapon = objects.SleepFang(0, 0, self)
        self.path_finding = None
        self.path_finding = PathFinding.PathFinding(self.maze.maze)
        self.init_fsm()

    def init_fsm(self):
        self.fsm = FSM(self)
        self.fsm.states["Idle"] = Idle(self)
        self.fsm.states["Approach"] = Approach(self)
        self.fsm.states["Attack"] = Attack(self)
        self.fsm.states["Flee"] = Flee(self)

        self.fsm.transitions["IdleToApproach"] = Transition("Approach")
        self.fsm.transitions["ApproachToAttack"] = Transition("Attack")
        self.fsm.transitions["ApproachToIdle"] = Transition("Idle")
        self.fsm.transitions["AttackToFlee"] = Transition("Flee")
        self.fsm.transitions["FleeToIdle"] = Transition("Idle")

        self.fsm.set_state("Idle")

    def change_state(self):

        now = pygame.time.get_ticks()

        if now - self.last_movement < self.MOVEMENT_THRESHOLD - self.DEX:
            return

        self.HP += 5
        if self.HP > self.total_max_hp():
            self.HP = self.total_max_hp()

        self.MP += 2
        if self.MP > self.MAX_MP:
            self.MP = self.MAX_MP

        if self.path == [] or now - self.last_path_finding > self.PATH_FINDING_INTERVAL:
            # self.path_finding.setStartEnd(self.row, self.col, self.player.row, self.player.col)
            # self.path = self.path_finding.aStar()
            self.path = self.path_finding.dijkstra(self.row, self.col, self.player.row, self.player.col)
            self.current_step = 0
            self.last_path_finding = now

        if self.idling:

            if (now - self.last_telescope > self.TELESCOPE_INTERVAL and self.telescope()) \
                    or distance_to(self.row, self.col, self.player.row, self.player.col) < 15:
                self.fsm.transition("IdleToApproach")
                self.idling = False
                self.seeking = True
                self.attacking = False
                self.fleeing = False
                self.awake_time = now

        if self.seeking:
            if len(self.path) < 10:
                self.fsm.transition("ApproachToAttack")
                self.idling = False
                self.seeking = False
                self.attacking = True
                self.fleeing = False
                self.awake_time = now

            if now - self.awake_time > self.LARGEST_AWAKE_TIME:
                self.fsm.transition("ApproachToIdle")
                self.idling = True
                self.seeking = False
                self.attacking = False
                self.fleeing = False

        if self.attacking:
            if self.HP < self.MAX_HP / 4 and randint(0, 3) == 0:
                self.fsm.transition("AttackToFlee")
                self.seeking = False
                self.attacking = False
                self.fleeing = True
                self.awake_time = now

        if self.fleeing:
            if distance_to(self.row, self.col, self.player.row, self.player.col) > 20:      # consider revise
                self.fsm.transition("FleeToIdle")
                self.awake_time = now
                self.idling = True
                self.seeking = False
                self.attacking = False
                self.fleeing = False
                self.awake_time = now

        self.fsm.execute()
        self.last_movement = now

    def telescope(self):
        row = randint(0, MAX_ROW)
        col = randint(0, MAX_COL)
        return row <= self.player.row <= row + 10 and col <= self.player.col <= col + 10

    def meteor(self):

        generated_row = self.player.row - 3
        generated_col = self.player.col + 3

        if generated_row < 0 or generated_col > 65 or self.MP < 50:
            return

        self.MP -= 50
        sorcery = objects.Meteorite(generated_row, generated_col, self.maze, self, self.player)
        self.maze.bullet_list.append(sorcery)

    def arcane_blast(self):

        if self.MP < 10:
            return
        self.MP -= 10
        sorcery = objects.Sorcery(self.row, self.col, self.orientation, self.maze, self, self.player)
        self.maze.bullet_list.append(sorcery)

    def attack(self):
        if self.is_in_one_line():
            if self.row < self.player.row:
                self.orientation = DOWN
            elif self.row > self.player.row:
                self.orientation = UP
            elif self.col < self.player.col:
                self.orientation = RIGHT
            else:
                self.orientation = LEFT
            self.arcane_blast()
        elif distance_to(self.row, self.col, self.player.row, self.player.col) < 5:
            self.flee()
        else:
            self.meteor()

    def is_in_one_line(self):
        if self.row == self.player.row:
            for i in range(min(self.col, self.player.col), max(self.col, self.player.col)+1):
                if self.maze.is_wall(self.row, i):
                    return False
            return True
        elif self.col == self.player.col:
            for i in range(min(self.row, self.player.row), max(self.row, self.player.row)+1):
                if self.maze.is_wall(i, self.col):
                    return False
            return True
        return False

    def path_seeking(self):
        if distance_to(self.row, self.col, self.player.row, self.player.col) < 10 and randint(0, 2) == 0:
            print(distance_to(self.row, self.col, self.player.row, self.player.col))
            print(self.row, self.col, self.player.row, self.player.col)
            self.meteor()
        else:
            Monster.path_seeking(self)

    def died(self):

        # Considered Modified.
        dropped = None
        odd = randint(0, 3)
        if odd == 0:
            dropped = objects.HitPointPotion(self.row, self.col)
        elif odd == 1:
            dropped = objects.MagicPointPotion(self.row, self.col)

        if dropped is not None:
            self.maze.object_list.append(dropped)
            self.maze.maze[self.row][self.col] = 8
        self.maze.monster_list.remove(self)

    def display(self):
        image = get_image('mage.jpg')
        image = pygame.transform.flip(image, True, False)
        if self.orientation == DOWN:
            image = pygame.transform.rotate(image, -90)
        elif self.orientation == UP:
            image = pygame.transform.rotate(image, 90)
        elif self.orientation == LEFT:
            image = pygame.transform.flip(image, True, False)
        self.maze.screen.blit(image, (self.col * 20, self.row * 20), [0, 0, 20, 20])

        pygame.draw.rect(self.maze.screen, RED, [self.col * 20 - 15, self.row * 20 - 14, 50, 5])
        pygame.draw.rect(self.maze.screen, GREEN,
                         [self.col * 20 - 15, self.row * 20 - 14, 50 * (self.HP / self.total_max_hp()), 5])
        pygame.draw.rect(self.maze.screen, RED, [self.col * 20 - 15, self.row * 20 - 9, 50, 5])
        pygame.draw.rect(self.maze.screen, BLUE,
                         [self.col * 20 - 15, self.row * 20 - 9, 50 * (self.MP / self.MAX_MP), 5])


class SkullKnight(Monster):

    def display(self):
        return










