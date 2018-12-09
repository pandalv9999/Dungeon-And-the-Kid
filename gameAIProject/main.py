import sys
import pygame
from pygame.locals import *
from gameAIProject import maze, actors, objects

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

SIZE = [1300, 800]
PAUSE = False

IMAGE_LIBRARY = {}


def get_image(path):
    global IMAGE_LIBRARY
    image = IMAGE_LIBRARY.get(path)
    if image is None:
        image = pygame.image.load(path)
        IMAGE_LIBRARY[path] = image
    return image


def equip_or_use(player, num):
    if len(player.inventory) > num:
        o = player.inventory[num]
        if isinstance(o, objects.Potions) or isinstance(o, objects.Scrolls):
            if not isinstance(o, objects.ScrollsOfResurrection):
                o.use()
                player.inventory.remove(o)
        elif isinstance(o, objects.Weapons):
            if not isinstance(player.shield, objects.TowerShield):
                if isinstance(o, objects.HeavySword):
                    player.inventory.append(player.shield)
                    player.shield = None
                temp = player.weapon
                player.weapon = o
                player.inventory.remove(o)
                if temp is not None:
                    player.inventory.append(temp)
        elif isinstance(o, objects.Armors):
            if isinstance(o, objects.RoundShield) or isinstance(o, objects.TowerShield):
                if not isinstance(player.weapon, objects.HeavySword):
                    if isinstance(o, objects.TowerShield):
                        if player.weapon is not None:
                            player.inventory.append(player.weapon)
                            player.weapon = None
                    temp = player.shield
                    player.shield = o
                    player.inventory.remove(o)
                    if temp is not None:
                        player.inventory.append(temp)
            else:
                temp = player.armor
                player.armor = o
                player.inventory.remove(o)
                if temp is not None:
                    player.inventory.append(temp)


def throw_last(player):
    if player.maze.maze[player.row][player.col] == 0 and len(player.inventory) > 0:
        o = player.inventory[len(player.inventory) - 1]
        player.inventory.remove(o)
        o.row = player.row
        o.col = player.col
        o.owner = None
        player.maze.object_list.append(o)
        if isinstance(o, objects.Armors):
            player.maze.maze[player.row][player.col] = 6
        if isinstance(o, objects.Weapons):
            player.maze.maze[player.row][player.col] = 7
        if isinstance(o, objects.Potions):
            player.maze.maze[player.row][player.col] = 8
        if isinstance(o, objects.Scrolls):
            player.maze.maze[player.row][player.col] = 9


def show_status(screen, player):

    global PAUSE

    while PAUSE:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # display player's status

        caption = "Status: "
        font = pygame.font.SysFont("times", 50)
        caption = font.render(caption, True, WHITE)
        screen.blit(caption, (100, 100))

        health = "HP: " + str(player.HP) + "/" + str(player.total_max_hp())
        font = pygame.font.SysFont("times", 30)
        health = font.render(health, True, WHITE)
        screen.blit(health, (120, 180))
        pygame.draw.rect(screen, RED, [320, 180, 300, 20])
        pygame.draw.rect(screen, GREEN, [320, 180, 300 * (player.HP / player.total_max_hp()), 20])

        magic = "MP: " + str(player.MP) + "/" + str(player.MAX_MP)
        font = pygame.font.SysFont("times", 30)
        magic = font.render(magic, True, WHITE)
        screen.blit(magic, (120, 210))
        pygame.draw.rect(screen, RED, [320, 210, 300, 20])
        pygame.draw.rect(screen, BLUE, [320, 210, 300 * (player.MP / player.MAX_MP), 20])

        experience = "EXP: " + str(player.EXP) + "/" + str(player.get_max_exp())
        font = pygame.font.SysFont("times", 30)
        experience = font.render(experience, True, WHITE)
        screen.blit(experience, (120, 240))
        pygame.draw.rect(screen, RED, [320, 240, 300, 20])
        pygame.draw.rect(screen, YELLOW, [320, 240, 300 * (player.EXP / player.get_max_exp()), 20])

        image = get_image('kid_large.jpg')
        screen.blit(image, (350, 280), [0, 0, 200, 200])

        text = "LVL: " + str(player.level)
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 300))

        text = "STR: " + str(player.total_str())
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 330))

        text = "DEF: " + str(player.total_def())
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 360))

        text = "INT: " + str(player.total_int())
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 390))

        text = "DEX: " + str(player.total_dex())
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 420))

        text = "(w) ARMOR: " + str(player.armor)
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 500))

        text = "(x) WEAPON: " + str(player.weapon)
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 530))

        text = "(y) SHIELD: " + str(player.shield)
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 560))

        text = "Press 'z' to resume game. "
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (120, 630))

        text = "Press corresponding button to equip"
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (120, 650))

        text = "or use items in inventory, "
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (150, 670))

        text = "or un_equip items. "
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (150, 690))

        text = "Press 'u' to throw last items in inventory"
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (120, 710))

        caption = "Inventory"
        font = pygame.font.SysFont("times", 50)
        caption = font.render(caption, True, WHITE)
        screen.blit(caption, (700, 100))

        number = 97
        start = 180

        for o in player.inventory:
            text = chr(number) + ".   " + str(o)
            font = pygame.font.SysFont("times", 30)
            text = font.render(text, True, WHITE)
            screen.blit(text, (720, start))
            number += 1
            start += 27

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            PAUSE = False
        elif keys[pygame.K_a]:
            equip_or_use(player, 0)
        elif keys[pygame.K_b]:
            equip_or_use(player, 1)
        elif keys[pygame.K_c]:
            equip_or_use(player, 2)
        elif keys[pygame.K_d]:
            equip_or_use(player, 3)
        elif keys[pygame.K_e]:
            equip_or_use(player, 4)
        elif keys[pygame.K_f]:
            equip_or_use(player, 5)
        elif keys[pygame.K_g]:
            equip_or_use(player, 6)
        elif keys[pygame.K_h]:
            equip_or_use(player, 7)
        elif keys[pygame.K_i]:
            equip_or_use(player, 8)
        elif keys[pygame.K_j]:
            equip_or_use(player, 9)
        elif keys[pygame.K_k]:
            equip_or_use(player, 10)
        elif keys[pygame.K_l]:
            equip_or_use(player, 11)
        elif keys[pygame.K_m]:
            equip_or_use(player, 12)
        elif keys[pygame.K_n]:
            equip_or_use(player, 13)
        elif keys[pygame.K_o]:
            equip_or_use(player, 14)
        elif keys[pygame.K_p]:
            equip_or_use(player, 15)
        elif keys[pygame.K_q]:
            equip_or_use(player, 16)
        elif keys[pygame.K_r]:
            equip_or_use(player, 17)
        elif keys[pygame.K_s]:
            equip_or_use(player, 18)
        elif keys[pygame.K_t]:
            equip_or_use(player, 19)
        elif keys[pygame.K_w]:
            if player.armor is not None and len(player.inventory) <= 20:
                player.inventory.append(player.armor)
                player.armor = None
        elif keys[pygame.K_x]:
            if player.weapon is not None and len(player.inventory) <= 20:
                player.inventory.append(player.weapon)
                player.weapon = None
        elif keys[pygame.K_y]:
            if player.shield is not None and len(player.inventory) <= 20:
                player.inventory.append(player.shield)
                player.shield = None
        elif keys[pygame.K_u]:
            throw_last(player)

        pygame.display.update()


def death_screen(screen, player):

    global PAUSE

    while PAUSE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        image = get_image('gameover.jpg')
        screen.blit(image, (450, 280))
        pygame.display.update()


def start_screen(screen):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_s]:
            return

        screen.fill(BLACK)

        text = "Dungeon And the Kid"
        font = pygame.font.Font("ancient.ttf", 100)
        text = font.render(text, True, RED)
        screen.blit(text, (270, 100))

        image = get_image('kid.jpg')
        screen.blit(image, (270, 300))

        image = get_image('sorcery.jpg')
        screen.blit(image, (400, 300))

        image = get_image('sorcery.jpg')
        screen.blit(image, (560, 300))

        image = get_image('sorcery.jpg')
        screen.blit(image, (690, 350))

        image = get_image('sorcery.jpg')
        screen.blit(image, (810, 300))

        image = get_image('goblin.jpg')
        screen.blit(image, (1050, 300))

        image = get_image('mage.jpg')
        screen.blit(image, (1070, 350))

        image = get_image('metero.jpg')
        screen.blit(image, (750, 250))

        image = get_image('metero.jpg')
        screen.blit(image, (850, 270))

        image = get_image('metero.jpg')
        screen.blit(image, (830, 370))

        image = get_image('metero.jpg')
        screen.blit(image, (900, 350))

        text = "Press 'w', 's', 'a', 'd' to control the kid to move UP, DOWN, LEFT, RIGHT"
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 600))

        text = "Press 'j' to melee attack. Press 'k' to range attack. (Only valid when ranged weapon is equipped.)"
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 630))

        text = "Press 'i' to get Status. Press 'p' to pick up objects."
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 660))

        text = "When standing on stairs, press 'n' to go to the next levels."
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 690))

        text = "Press 'ENTER' or 's' to start game. Good Luck!~"
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 720))

        pygame.display.update()


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Dungeon")

    current_lvl = 0
    background = maze.Maze(screen, current_lvl)
    player = actors.Player(background)
    background.add_player(player)
    background.add_monsters()
    start_screen(screen)

    move_time = 0

    while True:

        screen.fill(BLACK)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # player take actions.

        if pygame.time.get_ticks() - move_time > (200 - player.DEX):   # depends by DEX. 200. for test, 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move(LEFT)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move(RIGHT)
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                player.move(UP)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.move(DOWN)
            elif keys[pygame.K_p]:
                player.pick_up()
            elif keys[pygame.K_j]:
                player.melee_attack()
            elif keys[pygame.K_k]:
                player.sorcery_attack()
            elif keys[pygame.K_1]:
                player.cheat()
            elif keys[pygame.K_i]:
                PAUSE = True
                show_status(screen, player)
            elif keys[pygame.K_n]:
                if background.is_stair(player.row, player.col):
                    current_lvl += 1
                    del background
                    background = maze.Maze(screen, current_lvl)
                    player.maze = background
                    background.add_player(player)
                    background.add_monsters()
                    continue
            player.MP += 2
            player.HP += 5
            if player.HP >= player.total_max_hp():
                player.HP = player.total_max_hp()
            if player.MP >= player.MAX_MP:
                player.MP = player.MAX_MP
            move_time = pygame.time.get_ticks()

        if player.HP <= 0:
            PAUSE = True
            death_screen(screen, player)

        for monsters in background.monster_list:
            monsters.change_state()

        for bullet in background.bullet_list:
            bullet.proceeds()

        background.display()
        pygame.display.update()












