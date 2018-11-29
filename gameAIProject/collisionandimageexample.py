from pygame.locals import *
from random import randint
import pygame
import time
import math


class Cherry:
    '''
    defines the class of Cherry
    '''
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # initiates the place of an cherry

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))
        # draw the cherry


class Player:
    x = 0
    y = 0
    step = 30
    direction = 0

    def __init__(self):
        self.x = 750
        self.y = 750

    def update(self):

        # update position of head of snake
        if self.direction == 0:
            self.x = self.x + self.step
        if self.direction == 1:
            self.x = self.x - self.step
        if self.direction == 2:
            self.y = self.y - self.step
        if self.direction == 3:
            self.y = self.y + self.step
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > 750:
            self.x = 750
        if self.y > 550:
            self.y = 550

    # the 4 direction of the snake's basic movement
    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))
    # draw the snake on the game board


class Monster:
    '''
    adding a snake ai
    '''
    x = 10
    y = 10
    vx = 0
    vy = 0
    ax = 0
    ay = 0
    step = 10
    direction = 0

    updateCountMax = 2
    updateCount = 0
    targetX = 0
    targetY = 0

    def __init__(self):
        # the same process as a player snake
        # initial positions, no collision.
        self.x = 500
        self.y = 500

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # # update position of head of snake
        # if self.direction == 0:
        #     self.x = self.x + self.step
        # if self.direction == 1:
        #     self.x = self.x - self.step
        # if self.direction == 2:
        #     self.y = self.y - self.step
        # if self.direction == 3:
        #     self.y = self.y + self.step
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > 750:
            self.x = 750
        if self.y > 550:
            self.y = 550

    # def moveRight(self):
    #     self.direction = 0
    #
    # def moveLeft(self):
    #     self.direction = 1
    #
    # def moveUp(self):
    #     self.direction = 2
    #
    # def moveDown(self):
    #     self.direction = 3

    def target(self, dx, dy):
        '''
        :param dx:
        :param dy:
        :return:
        '''
        maxAcceleration = 2
        tmpvx = dx - self.x
        tmpvy = dy - self.y
        if abs(float(tmpvx)) !=0:
            self.ax = float(tmpvx) / abs(float(tmpvx)) * maxAcceleration
        if abs(float(tmpvy)) !=0:
            self.ay = float(tmpvy) / abs(float(tmpvy)) * maxAcceleration
        # t = float(tmpvy) / float(tmpvx)

        self.vx += self.ax
        xflag = False
        if self.vx < 0:
            xflag = True
        self.vy += self.ay
        yflag = False
        if self.vy < 0:
            yflag = True
        self.vx = min(float(self.step), abs(self.vx))
        self.vy = min(float(self.step), abs(self.vy))
        if xflag:
            self.vx = -self.vx
        if yflag:
            self.vy = -self.vy


    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Game:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 - bsize and x1 <= x2 + bsize:
            if y1 >= y2 - bsize and y1 <= y2 + bsize:
                return True
        return False


class App:
    windowWidth = 800
    windowHeight = 600
    player = 0
    cherry = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._cherry_surf = None
        self.game = Game()
        self.player = Player()
        self.cherry = Cherry(200, 200)
        self.monster = Monster()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Player versus Monster demo')
        self._running = True
        self._human_surf = pygame.image.load("human.png").convert()  # load the picture of player
        self._monster_surf = pygame.image.load("monster.png").convert()  # load the picture of monster
        self._cherry_surf = pygame.image.load("cherry.png").convert()  # load the picture of cherry

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.monster.target(self.player.x, self.player.y)
        self.player.update()
        self.monster.update()

        # does player eat apple?
        if self.game.isCollision(self.cherry.x, self.cherry.y, self.player.x, self.player.y, 40):
            self.cherry.x = randint(2, 9) * 44
            self.cherry.y = randint(2, 9) * 44

        # does monster eat apple? the monster snake will not grow
        # if self.game.isCollision(self.cherry.x, self.cherry.y, self.monster.x, self.monster.y, 30):
        #     self.cherry.x = randint(2, 9) * 44
        #     self.cherry.y = randint(2, 9) * 44

        # does snake collide with itself?
        if self.game.isCollision(self.player.x, self.player.y, self.monster.x, self.monster.y, 30):
            print "You catch the monster! Collision: "
            print "player(" + str(self.player.x) + "," + str(self.player.y) + ")"
            print "monster(" + str(self.monster.x) + "," + str(self.monster.y) + ")"
            # exit(0)

    pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf, self._human_surf)
        self.monster.draw(self._display_surf, self._monster_surf)
        self.cherry.draw(self._display_surf, self._cherry_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            # the direction button on the keyboard determines the movement of the player
            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0)  # keeps everything from moving too fast
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
