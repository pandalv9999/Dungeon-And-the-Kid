import sys
import pygame
from pygame.locals import *
from gameAIProject import Maze, objects

SIZE = [1300, 800]

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Dungeon")

    background = Maze.Maze(screen, 0)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        background.display()
        pygame.display.update()



