import pygame
from const import *

class Block(pygame.sprite.Sprite):
    def __init__(self, blockType, rowIdx, colIdx, relativePos):
        super(Block, self).__init__()
        self.blockType = blockType
        self.image = pygame.image.load( BLOCK_RES_FMT % blockType )
        self.image = pygame.transform.scale(self.image, (SPRITE_SIZE_W, SPRITE_SIZE_H))
        self.rect = self.image.get_rect()
        self.rect.x = relativePos[1] + colIdx * self.rect.width
        self.rect.y = relativePos[0] + rowIdx * self.rect.height
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def GetBlockType(self):
        return self.blockType
        
    def GetRect(self):
        return self.rect