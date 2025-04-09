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
    
    # 处理键盘事件
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT] or pressed[K_RIGHT]:
        game.player.update()
    
    # 处理鼠标事件
    for event in pygame.event.get(MOUSEBUTTONDOWN):
        if event.type == MOUSEBUTTONDOWN:
            # 传递鼠标点击事件给游戏对象处理
            pygame.event.post(event)
