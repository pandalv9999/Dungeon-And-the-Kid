import sys
import pygame
from pygame.locals import *
from gameAIProject import maze, actors

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

BLACK = (0, 0, 0)

SIZE = [1300, 800]

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Dungeon")

    background = maze.Maze(screen, 0)
    player = actors.Player(background)
    background.add_player(player)

    move_time = 0

    while True:

        background.screen.fill(BLACK)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # player take actions.

        if pygame.time.get_ticks() - move_time > (200 - player.DEX):   # depends by DEX
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
            move_time = pygame.time.get_ticks()

        background.display()
        pygame.display.update()



