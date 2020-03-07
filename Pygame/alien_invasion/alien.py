import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        # 继承父类
        super().__init__()
        # 初始化外星人并设置其初始位置
        self.ai_setting = ai_setting
        self.screen = screen
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # 不需要再次设定屏幕矩形，在ship模块中已经建立了屏幕矩形。本类带入其他模块后可以直接通过参数screen调用
        # 建立外星人的初始坐标，因为没有建立screen的矩形属性，因此不能调用screen矩形坐标位置作为参照
        # 以下代码是将外星人矩形的左上角坐标x,y放置在屏幕左上角位置附近，起始放置图像的位置，但是还没有绘制出来
        # 实际上x,y是矩形距离左上角坐标(0,0)的横,纵坐标距离值
        # 以外星人矩形自身的宽和高设置其距离左边缘和上边缘的边距
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 设置外星人的准确位置,只浮点化了rect.x却没有浮点化rect.y，为什么？
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_setting.alien_speed_factor*self.ai_setting.fleet_direction)
        self.rect.x = self.x

    # 在指定位置绘制外星人
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
