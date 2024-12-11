import pygame
from pygame.locals import *
from utils import *
from const import *


class Player(pygame.sprite.Sprite):
    def __init__(self, imgPaths, x, y, xMin, xMax):
        super(Player, self).__init__()
        self.images = []
        self.imageIndex = 0
        self.posX = x
        self.posY = y
        self.posXMin = xMin
        self.posXMax = xMax
        self.preChangeTime = getCurrentTime()
        for path in imgPaths:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (PLAYER_SIZE_W, PLAYER_SIZE_H))
            self.images.append( img )


    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            if self.posX > self.posXMin:
                self.posX -= 7
        if pressed[K_RIGHT]:
            if self.posX < self.posXMax:
                self.posX += 7
        
        if getCurrentTime() - self.preChangeTime > 200:
            self.preChangeTime = getCurrentTime()
            self.imageIndex = (self.imageIndex + 1) % len(self.images)


    def GetRect(self):
        image = self.images[ self.imageIndex ]
        rect = image.get_rect()
        rect.x = self.posX
        rect.y = self.posY
        return rect


    def draw(self, surface):
        image = self.images[ self.imageIndex ]
        surface.blit(image, self.GetRect())
