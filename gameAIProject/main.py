import sys
import pygame
from pygame.locals import *
from gameAIProject import maze, actors

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
        pygame.draw.rect(screen, GREEN, [320, 180, 300 * (player.HP / player.MAX_HP), 20])

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

        text = "ARMOR: " + str(player.armor)
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 500))

        text = "WEAPON: " + str(player.weapon)
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 530))

        text = "SHIELD: " + str(player.shield)
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, WHITE)
        screen.blit(text, (120, 560))

        text = "Press 'z' to resume game. "
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (120, 650))

        text = "Press corresponding button to equip"
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (120, 670))

        text = "or use items in inventory."
        font = pygame.font.SysFont("times", 30)
        text = font.render(text, True, YELLOW)
        screen.blit(text, (150, 690))

        caption = "Inventory"
        font = pygame.font.SysFont("times", 50)
        caption = font.render(caption, True, WHITE)
        screen.blit(caption, (700, 100))

        number = 97
        start = 180

        for objects in player.inventory:
            text = chr(number) + ".   " + str(objects)
            font = pygame.font.SysFont("times", 30)
            text = font.render(text, True, WHITE)
            screen.blit(text, (720, start))
            number += 1
            start += 27

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            PAUSE = False

        pygame.display.update()


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Dungeon")

    background = maze.Maze(screen, 0)
    player = actors.Player(background)
    background.add_player(player)

    move_time = 0

    while True:

        screen.fill(BLACK)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # player take actions.

        if pygame.time.get_ticks() - move_time > (0 - player.DEX):   # depends by DEX. 200. for test, 0
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
            elif keys[pygame.K_i]:
                PAUSE = True
                show_status(screen, player)
                pygame.draw.rect(screen, BLACK, [300, 300, 700, 200])
            move_time = pygame.time.get_ticks()

        background.display()
        pygame.display.update()











