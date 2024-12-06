import pygame
from pygame.locals import *
from utils import *
from const import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, imgPath, x, y, dirX, dirY):
        super(Ball, self).__init__()
        self.posX = x
        self.posY = y
        self.dirX = dirX
        self.dirY = dirY
        self.speed = 0.3
        img = pygame.image.load(imgPath)
        img = pygame.transform.scale(img, (SPRITE_SIZE_W, SPRITE_SIZE_H))
        self.image = img
        self.rect = img.get_rect()
        self.preRotateTime = getCurrentTime()
        self.jntmSound = pygame.mixer.Sound(SoundRes.JNTM)
        self.ngmSound = pygame.mixer.Sound(SoundRes.NGM)
    
    def SetSpeed(self, speed):
        self.speed = speed
    
    def GetRect(self):
        return self.rect

    def update(self):
        self.posX += self.speed * self.dirX
        self.posY += self.speed * self.dirY
        self.rect.x = self.posX
        self.rect.y = self.posY

        if getCurrentTime() - self.preRotateTime > 50:
            self.preRotateTime = getCurrentTime()
            self.image = pygame.transform.rotate( self.image, (getCurrentTime() % 4 - 2) * 90)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def changeDirection(self, rect):
        self.jntmSound.play()
        if abs(self.GetRect().x - rect.x) <= abs(self.GetRect().y - rect.y):
            self.dirY *= -1
        else:
            self.dirX *= -1

    def changeYDirection(self, rect):
        self.ngmSound.play()
        if abs(self.GetRect().x - rect.x) <= abs(self.GetRect().y - rect.y):
            self.dirY *= -1
        else:
            self.dirX *= -1
            if self.dirY > 0:
                self.dirY *= -1