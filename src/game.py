import pygame
from pygame.locals import *
from const import *
from player import *
from ball import *
from level import *
from block import *
import random


class Game(object):
    def __init__(self, surface):
        pygame.mixer.init()
        self.surface = surface
        self.Load(1)
        self.surface = surface
        self.game_over = False
        self.restart_button = pygame.Rect(0, 0, 150, 50)  

    def Load(self, lv):
        self.level = Level(lv)
        self.isGameOver = False
        self.balls = []
        self.loadPlayer()
        self.loadOneBall(self.player.GetRect().x, self.player.GetRect().y - SPRITE_SIZE_H - 5, 1, -1)
        self.loadBlockImages()


    def loadPlayer(self):
        self.player = Player(
            PLAYER_RES, 
            (GAME_SIZE[0] - PLAYER_SIZE_W)/2, GAME_SIZE[1] - PLAYER_SIZE_H, 
            SPRITE_SIZE_W, GAME_SIZE[0] - PLAYER_SIZE_W - SPRITE_SIZE_W)


    def loadBlockImages(self):
        self.blocks = []
        for block in self.level.GetBlocks():
            sp = Block(block[2], block[0], block[1], (0, 0))
            self.blocks.append(sp)


    def loadOneBall(self, x, y, dirX, dirY):
        # 生成随机的水平方向，-1 或 1
        dirX = random.choice([-1, 1])
        ball = Ball(BALL_RES, x, y, dirX, -1)
        self.balls.append(ball)


    def draw(self):
        if self.isGameOver:
            img = pygame.image.load(GAME_OVER_RES)
            self.surface.blit(img, img.get_rect())
            # 绘制绿色的重新开始按钮
            pygame.draw.rect(self.surface, (0, 255, 0), self.restart_button)  
            # 使用系统默认字体
            # 使用支持中文的字体，如 SimHei
            font = pygame.font.SysFont("SimHei", 20)
            text = font.render("你打球像蔡徐坤", True, (255, 255, 255))  # 按钮上的文字

            text_rect = text.get_rect(center=self.restart_button.center)
            self.surface.blit(text, text_rect)  # 绘制按钮上的文字
            return 
        self.player.draw(self.surface)
        [block.draw(self.surface) for block in self.blocks]
        [ball.draw(self.surface) for ball in self.balls]


    def update(self):
        if self.isGameOver:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        self.Load(1)
            return
        self.player.update()
        [ball.update() for ball in self.balls]
        self.checkCollide()
        if self.isGameWin():
            self.Load( self.level.level + 1 )


    def checkBallBlockCollide(self):
        for ball in self.balls:
            for block in self.blocks:
                if ball.GetRect().colliderect( block.GetRect() ):
                    ball.changeDirection( block.GetRect() )
                    self.processBlock(ball, block)
                    break


    def processBlock(self, ball, block):
        if block.GetBlockType() == BlockType.COPY:
            self.copyBalls()
        if block.GetBlockType() == BlockType.SPEED_UP:
            ball.SetSpeed(1.5)
        if block.GetBlockType() == BlockType.SPEED_DOWN:
            ball.SetSpeed(0.2)
        if block.GetBlockType() == BlockType.WALL:
            return
        self.blocks.remove(block)


    def checkBallPlayerCollide(self):
        for ball in self.balls:
            if ball.GetRect().colliderect( self.player.GetRect() ):
                ball.changeYDirection( self.player.GetRect() )
                break


    def checkCollide(self):
        self.checkBallBlockCollide()
        self.checkBallPlayerCollide()


        flag = True
        while flag:
            flag = False
            for ball in self.balls:
                if ball.GetRect().y > GAME_SIZE[1]:
                    self.balls.remove(ball)
                    flag = True
                    break
        if len(self.balls) == 0:
            self.isGameOver = True


    def copyBalls(self):
        balls = [ball for ball in self.balls]
        for ball in balls:
            self.loadOneBall(ball.GetRect().x, ball.GetRect().y, 1, -1)


    def isGameWin(self):
        for block in self.blocks:
            if block.GetBlockType()!= BlockType.WALL:
                return False
        return True
