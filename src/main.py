import pygame, sys
from pygame.locals import *
from game import *
from const import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode(GAME_SIZE)
pygame.display.set_caption('打砖块')
game = Game(DISPLAYSURF)

clock = pygame.time.Clock()

while True:
    if pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    
    DISPLAYSURF.fill((255, 255, 255))
    game.update()
    game.draw()
    pygame.display.update()
    clock.tick(60)
