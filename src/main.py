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
    # 事件处理移到 game.update() 中
    # if pygame.event.get(QUIT):
    #     pygame.quit()
    #     sys.exit()
    
    # 背景填充已移到 game.update() 中
    # DISPLAYSURF.fill((255, 255, 255))
    game.update() # game.update() 内部会处理事件、背景和玩家更新
    game.draw() # game.draw() 只负责绘制游戏元素
    pygame.display.update()
    clock.tick(60)
    
    # 移除冗余的键盘处理
    # pressed = pygame.key.get_pressed()
    # if pressed[K_LEFT] or pressed[K_RIGHT]:
    #     game.player.update()
    
    # 移除冗余的鼠标处理
    # for event in pygame.event.get(MOUSEBUTTONDOWN):
    #     if event.type == MOUSEBUTTONDOWN:
    #         # 传递鼠标点击事件给游戏对象处理
    #         pygame.event.post(event) # post 是错误的用法，应该直接处理
