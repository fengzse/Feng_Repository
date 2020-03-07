"""位置参数的顺序一定不能出错，必须严格按照程序指令指向先后设置位置参数，否则程序不能运行，会使代码找不到映射"""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_setting, screen, ship):
        super().__init__()
        # 建立屏幕属性
        self.screen = screen
        # 子弹不是添加的图像，是自己创建的，因此需要创建矩形，参数包括左上角坐标和其他构成参数
        # x,y是矩形距离左上角坐标(0,0)的横,纵坐标距离值
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_height)
        # 将子弹位置对应为飞船位置
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 将子弹飞行坐标(y)小数化，便于微调
        self.y = float(self.rect.y)

        # 设定子弹颜色，速度等数据
        self.bullet_color = ai_setting.bullet_color
        self.bullet_speed = ai_setting.bullet_speed_factor

    # 设定子弹移动，并绘制出子弹
    def update(self):
        self.y -= self.bullet_speed
        # 游戏只接收矩形参数，子弹的移动位置必须由rect.y表示，self.y只是为了接收小数位使用的中间变量
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)
