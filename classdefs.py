import numpy as np
import matplotlib.pyplot as plt
import pygame
import random

class Drone(pygame.sprite.Sprite):
    def __init__(self, xi, yi, zi, mode):
        self.x = xi
        self.y = yi
        self.z = zi
        self.mode = mode
        super(Drone, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 191, 255))
        self.rect = self.surf.get_rect(
            center=(xi,yi,)
        )

        self.direction = np.pi / 2
        #self.direction = random.randint(0,43) / 7
        self.force = 10

        self.l = self.rect.left
        self.t = self.rect.top
        self.prevl = self.l
        self.prevt = self.t

    def update(self,SCREEN_WIDTH, SCREEN_HEIGHT):

        self.prevl = self.l
        self.prevt = self.t


        if self.mode==0:
            self.direction=0
            self.force=0
        elif self.mode==1:
            self.direction = random.randint(0,43) / 7
            self.force = 10
        elif self.mode==2:
            self.direction = 0
            self.force = 10

        if self.force > 0:
            dx = round(self.force * np.cos(self.direction))
            dy = -1*round(self.force * np.sin(self.direction))
            self.rect.move_ip(dx,dy)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.l = self.rect.left
        self.t = self.rect.top

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, z):
        super(Goal, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((57,255,20))
        self.rect = self.surf.get_rect(
            center=(x,y,)
        )

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,z,xdim,ydim,zdim):
        super(Obstacle, self).__init__()
        self.surf = pygame.Surface((xdim,ydim))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(
            center=(x,y,)
        )

class Scanner(pygame.sprite.Sprite):
    def __init__(self,left,top,xdim,ydim,dir):
        super(Scanner, self).__init__()
        self.surf = pygame.Surface((xdim,ydim))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.dir = dir

    def update(self):
        if self.dir == "r":
            self.rect.move_ip(1,0)
        elif self.dir == "l":
            self.rect.move_ip(-1,0)
        elif self.dir == "u":
            self.rect.move_ip(0,-1)
        elif self.dir == "d":
            self.rect.move_ip(0,1)