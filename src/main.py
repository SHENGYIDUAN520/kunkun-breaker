import pygame, sys
from pygame.locals import *
from game import *
from const import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode(GAME_SIZE)
game = Game(DISPLAYSURF)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    game.update()
    DISPLAYSURF.fill( (255, 255, 255) )
    game.draw()
    pygame.display.update()
