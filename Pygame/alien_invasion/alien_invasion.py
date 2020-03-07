"""主模块的作用是建立运行函数，函数中包括pygame的初始化设定__init__和游戏的运行循环，也就是具体的运算函数，类都不在
主模块部分，这个模块只负责游游戏的运行，代码尽量简化，需要的类和函数从其他模块引入"""
# 位置参数的顺序一定不能出错，必须严格按照程序指令指向先后设置位置参数，否则程序不能运行，会使代码找不到映射

# import sys 将事件监视移入game_functions模块后，主程序中实际上不再需要 import sys
import pygame
from settings import AlienSettings
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

ai_setting = AlienSettings()


def run_game():
    # 初始化pygame，设置和屏幕对象
    pygame.init()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption('Alien Invasion')
    play_button = Button(ai_setting, screen, 'Play')
    ship = Ship(ai_setting, screen)

    bullets = Group()  # pygame.sprite中的Group类相当于一个编组列表
    aliens = Group()
    stats = GameStats(ai_setting)
    sb = ScoreBoard(ai_setting, screen, stats)
    # 创建外星人群, 不能放在下面的循环中创建，只要在循环前创建一批外星人就够了
    gf.create_fleets(ai_setting, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        # 监控事件
        gf.check_events(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets)
        # 检查激活状态，激活则继续执行下面的代码
        if stats.game_active:
            ship.update()
            # 直接调用game_function中的update_bullets函数
            gf.update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets)
            # 更新外星人的移动位置
            gf.update_aliens(ai_setting, screen, stats, sb, ship, aliens, bullets)
        # 每次循环都会重绘屏幕
        gf.update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
