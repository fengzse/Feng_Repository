"""这个模块掌管所有飞船的相关设定，如飞船的外形，位置，移动，射击等"""
# 位置参数的顺序一定不能出错，必须严格按照程序指令指向先后设置位置参数，否则程序不能运行，会使代码找不到映射
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_setting, screen):
        super().__init__()
        """初始化飞船并设置其初始位置"""
        self.screen = screen
        self.ai_setting = ai_setting
        # 加载飞船图像并获取其矩形属性
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 浮点化rect值，rect值是对应屏幕rect值的，这样self.center的赋值才有意义，然后再用center接受小数参数
        self.center = float(self.rect.centerx)
        # 添加moving_right的属性，并设置其为False,在类初始化方法中设定，而不是单独编写为一个方法
        self.moving_right = False
        # 默认值为false表明没有指令给飞船的时候，其移到判断为false
        self.moving_left = False
        # 设置左移

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 此句表明假定其为True且飞船矩形x坐标右边界小于屏幕右边界
            self.center += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            # 此处可以写为>0，因为屏幕矩形左边界的值就为0，左上角坐标为(0,0)
            self.center -= self.ai_setting.ship_speed_factor
        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
