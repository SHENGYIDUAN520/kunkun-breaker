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
        self.speed = 10  # 增加移动速度
        self.preChangeTime = getCurrentTime()
        for path in imgPaths:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (PLAYER_SIZE_W, PLAYER_SIZE_H))
            self.images.append(img)

    def update(self):
        pressed = pygame.key.get_pressed()
        # 使用更精确的边界检查，同时支持方向键和WASD
        if pressed[K_LEFT] or pressed[pygame.K_a]:  # 左方向键或A键
            new_x = self.posX - self.speed
            if new_x >= self.posXMin:
                self.posX = new_x
        if pressed[K_RIGHT] or pressed[pygame.K_d]:  # 右方向键或D键
            new_x = self.posX + self.speed
            if new_x <= self.posXMax:  # 移除多余的PLAYER_SIZE_W减法
                self.posX = new_x
        
        if getCurrentTime() - self.preChangeTime > 200:
            self.preChangeTime = getCurrentTime()
            self.imageIndex = (self.imageIndex + 1) % len(self.images)

    def GetRect(self):
        image = self.images[self.imageIndex]
        rect = image.get_rect()
        rect.x = self.posX
        rect.y = self.posY
        return rect

    def draw(self, surface):
        image = self.images[self.imageIndex]
        surface.blit(image, self.GetRect())
