import pygame
from pygame.locals import *
from const import *
from player import *
from ball import *
from level import *
from block import *
import random
import os
import cv2
import numpy as np
from PIL import Image  # 用于获取GIF信息
import time


class Game(object):
    def __init__(self, surface):
        pygame.mixer.init()
        self.surface = surface
        self.state = "START"
        self.Load(1)
        self.game_over = False
        
        # 先初始化按钮，确保基本UI可用
        # 按钮位置和大小
        button_width = 200
        button_height = 50
        center_x = GAME_SIZE[0] // 2 - button_width // 2
        
        self.start_button = pygame.Rect(center_x, 200, button_width, button_height)
        self.level_select_button = pygame.Rect(center_x, 300, button_width, button_height)
        self.exit_button = pygame.Rect(center_x, 400, button_width, button_height)
        self.restart_button = pygame.Rect(center_x, 75, button_width, button_height)
        self.home_button = pygame.Rect(20, 20, 100, 40)  # 返回主页按钮
        
        # 关卡选择按钮
        self.level_buttons = []
        self.setup_level_buttons()
        
        # 设置字体
        self.font = pygame.font.SysFont("SimHei", 24)
        
        # 加载GIF背景
        try:
            # 使用PIL打开GIF获取信息
            gif_path = "res/video/background.gif"
            pil_image = Image.open(gif_path)
            
            # 加载所有帧
            self.bg_frames = []
            self.frame_times = []
            
            # 保存原始尺寸用于缩放
            original_size = pil_image.size
            scale = min(GAME_SIZE[0]/original_size[0], GAME_SIZE[1]/original_size[1])
            target_size = (int(original_size[0]*scale), int(original_size[1]*scale))
            
            while True:
                try:
                    # 获取当前帧的持续时间
                    duration = pil_image.info.get('duration', 100)
                    if duration == 0:
                        duration = 100
                    self.frame_times.append(duration)
                    
                    # 转换当前帧为pygame surface
                    current_frame = pil_image.convert('RGBA')
                    # 转换为pygame surface
                    str_frame = current_frame.tobytes()
                    frame_surface = pygame.image.fromstring(str_frame, current_frame.size, 'RGBA')
                    # 缩放到目标尺寸
                    frame_surface = pygame.transform.scale(frame_surface, target_size)
                    self.bg_frames.append(frame_surface)
                    
                    # 移动到下一帧
                    pil_image.seek(pil_image.tell() + 1)
                    
                except EOFError:
                    break
            
            self.current_frame = 0
            self.last_frame_time = time.time() * 1000
            self.success_reading = True
            
            
        except Exception as e:
            print(f"背景GIF加载错误: {str(e)}")
            import traceback
            traceback.print_exc()  # 打印详细错误信息
            self.success_reading = False

    def setup_level_buttons(self):
        self.level_buttons.clear()
        cols = 10
        button_size = 50
        spacing = 10
        start_x = (GAME_SIZE[0] - (cols * (button_size + spacing))) // 2
        start_y = 100
        
        for i in range(59):
            row = i // cols
            col = i % cols
            x = start_x + col * (button_size + spacing)
            y = start_y + row * (button_size + spacing)
            self.level_buttons.append(pygame.Rect(x, y, button_size, button_size))

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
        if self.state == "START":
            self.draw_start_screen()
        elif self.state == "LEVEL_SELECT":
            self.draw_level_select()
        elif self.state == "PLAYING":
            if self.isGameOver:
                self.draw_game_over()
            else:
                self.draw_game()
                pygame.draw.rect(self.surface, (70, 70, 70), self.home_button)
                text = self.font.render("主页", True, (255, 255, 255))
                self.surface.blit(text, (self.home_button.centerx - text.get_width()//2, 
                                       self.home_button.centery - text.get_height()//2))

    def draw_start_screen(self):
        # 绘制视频背景
        if self.state == "START":
            self.update_video_background()
        
        # 如果没有视频背景，绘制纯色背景
        if not self.success_reading:
            self.surface.fill((0, 0, 0))
        
        # 绘制半透明黑色遮罩使按钮更容易看见
        s = pygame.Surface(GAME_SIZE)
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.surface.blit(s, (0,0))
        
        # 绘制按钮
        for button, text in [(self.start_button, "开始游戏"), 
                           (self.level_select_button, "选择关卡"),
                           (self.exit_button, "退出游戏")]:
            pygame.draw.rect(self.surface, (0, 255, 0), button)
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.surface.blit(text_surface, (button.centerx - text_surface.get_width()//2,
                                           button.centery - text_surface.get_height()//2))

    def draw_level_select(self):
        self.surface.fill((0, 0, 0))
        pygame.draw.rect(self.surface, (70, 70, 70), self.home_button)
        home_text = self.font.render("主页", True, (255, 255, 255))
        self.surface.blit(home_text, (self.home_button.centerx - home_text.get_width()//2,
                                     self.home_button.centery - home_text.get_height()//2))
        
        for i, button in enumerate(self.level_buttons):
            pygame.draw.rect(self.surface, (0, 200, 0), button)
            text = self.font.render(str(i + 1), True, (255, 255, 255))
            self.surface.blit(text, (button.centerx - text.get_width()//2,
                                   button.centery - text.get_height()//2))

    def draw_game_over(self):
        img = pygame.image.load(GAME_OVER_RES)
        self.surface.blit(img, img.get_rect())
        pygame.draw.rect(self.surface, (0, 255, 0), self.restart_button)
        pygame.draw.rect(self.surface, (70, 70, 70), self.home_button)
        
        restart_text = self.font.render("重新开始", True, (255, 255, 255))
        home_text = self.font.render("主页", True, (255, 255, 255))
        
        self.surface.blit(restart_text, (self.restart_button.centerx - restart_text.get_width()//2,
                                       self.restart_button.centery - restart_text.get_height()//2))
        self.surface.blit(home_text, (self.home_button.centerx - home_text.get_width()//2,
                                     self.home_button.centery - home_text.get_height()//2))

    def draw_game(self):
        self.player.draw(self.surface)
        [block.draw(self.surface) for block in self.blocks]
        [ball.draw(self.surface) for ball in self.balls]

    def update(self):
        # 处理鼠标点击事件
        for event in pygame.event.get((MOUSEBUTTONDOWN,)):  # 只获取鼠标点击事件
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.state == "START":
                    if self.start_button.collidepoint(mouse_pos):
                        self.state = "PLAYING"
                        self.Load(1)
                    elif self.level_select_button.collidepoint(mouse_pos):
                        self.state = "LEVEL_SELECT"
                    elif self.exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
                
                elif self.state == "LEVEL_SELECT":
                    if self.home_button.collidepoint(mouse_pos):
                        self.state = "START"
                    else:
                        for i, button in enumerate(self.level_buttons):
                            if button.collidepoint(mouse_pos):
                                self.Load(i + 1)
                                self.state = "PLAYING"
                                break
                
                elif self.state == "PLAYING":
                    if self.isGameOver:
                        if self.restart_button.collidepoint(mouse_pos):
                            self.Load(self.level.level)
                        elif self.home_button.collidepoint(mouse_pos):
                            self.state = "START"
                    elif self.home_button.collidepoint(mouse_pos):
                        self.state = "START"

        # 游戏逻辑更新
        if self.state == "PLAYING" and not self.isGameOver:
            self.player.update()  # Player类内部会自己检查按键状态
            [ball.update() for ball in self.balls]
            self.checkCollide()
            if self.isGameWin():
                self.Load(self.level.level + 1)


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

    def update_video_background(self):
        if not hasattr(self, 'bg_frames') or not self.success_reading:
            self.surface.fill((0, 0, 0))
            return
            
        try:
            current_time = time.time() * 1000
            if current_time - self.last_frame_time >= self.frame_times[self.current_frame]:
                self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
                self.last_frame_time = current_time
               # print(f"切换到帧 {self.current_frame}")  # 调试信息
            
            # 计算显示位置（居中）
            frame = self.bg_frames[self.current_frame]
            x = (GAME_SIZE[0] - frame.get_width()) // 2
            y = (GAME_SIZE[1] - frame.get_height()) // 2
            self.surface.blit(frame, (x, y))
            
        except Exception as e:
            print(f"背景更新错误: {str(e)}")
            import traceback
            traceback.print_exc()
            self.success_reading = False

    def __del__(self):
        # 释放视频资源
        if hasattr(self, 'video'):
            self.video.release()
