"""控制游戏动作，输入的具体函数集合，每个函数相对独立。这个模块中不涉及游戏角色的设定和游戏设定，只负责编写行动代码"""
# 位置参数的顺序一定不能出错，必须严格按照程序指令指向先后设置位置参数，否则程序不能运行，会使代码找不到映射

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


# 代码重构将keydown和keyup分别进行检定，以应对将来代码复杂化
def check_keydown_events(event, ai_setting, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_setting, screen, ship, bullets)
    elif event.key == pygame.K_q:
        with open('High_score.txt') as file_object:
            file_object.read()
        sys.exit()


# 重构创建子弹实例的代码，将其从check_keydown_events中独立出来
def fire_bullets(ai_setting, screen, ship, bullets):
    if len(bullets) < ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_checked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_checked and not stats.game_active:
        ai_setting.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        # 重置游戏信息
        stats.reset_stats()
        stats.game_active = True
        # 重置所有得分版信息
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空所有外星人和子弹列表，并重新创建新的外星人群和飞船
        aliens.empty()
        bullets.empty()
        create_fleets(ai_setting, screen, ship, aliens)
        ship.center_ship()


# 具体针对飞船而不是整个游戏窗口坐检查后，check_events需要带入形参ship
def check_events(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets):
    # ship在这里只是一个形参，但是带回主模块的时候，ship=Ship(screen),是一个类实例。同时这个模块不用导入ship模块
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


# 这个函数不是定义屏幕的部分而是刷新屏幕显示的部分，定义屏幕的部分仍在主模块中
# 但是没有import 主模块，ship模块和settings模块，函数参数为什么可以使用？----与原模块没有直接联系，只有括号里的参数
# 能够在函数里被调用即可，具体执行会import到主模块中执行
def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button):
    # 每次循环都会重绘屏幕
    screen.fill(ai_setting.bg_colour)
    # 用遍历列表的方式绘制每一颗子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 显示新绘制的屏幕
    pygame.display.flip()


# 将主模块中关于子弹的部分尽可能地移入本模块
def update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets):
    # bullets编组调用update方法，但必须带回主模块，映射到Bullet类才能执行
    bullets.update()
    # 编写代码使子弹在越过屏幕上缘后被删除,注意应该清除bullets编组列表的副本而不是原列表中的元素
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_setting, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_setting, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    '''方法sprite.groupcollide() 将每颗子弹的rect 同每个外星人的rect 进行比较，并返回一个字典，其中包含发生了碰撞的子弹和
       外星人。在这个字典中，每个键都是一颗子弹，而相应的值都是被击中的外星'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # 检查外星人是否被全部消灭
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_setting.increase_speed()
        # 在所有外星人被消灭后，提高玩家等级
        stats.level += 1
        sb.prep_level()
        create_fleets(ai_setting, screen, ship, aliens)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def get_number_aliens_x(ai_setting, alien_width):
    # 计算一行可容纳多少个外星人,外星人间距为外星人宽度
    available_space_x = ai_setting.screen_width - (2 * alien_width)
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def get_number_rows(ai_setting, ship_height, alien_height):
    available_space_y = (ai_setting.screen_height - ship_height - 3 * alien_height)
    alien_rows = int(available_space_y / (2 * alien_height))
    return alien_rows


def creat_alien(ai_setting, screen, aliens, alien_number, row_number):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    # 在循环中给每个新创建的实例重新定位，rect.x,并将每个实例添加到aliens编组列表中
    alien.rect.x = alien.x
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)


def create_fleets(ai_setting, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_setting, screen)
    number_alien_x = get_number_aliens_x(ai_setting, alien.rect.width)
    alien_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)
    for row_number in range(alien_rows):
        for alien_number in range(number_alien_x):
            creat_alien(ai_setting, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        # 遍历中当有一个alien的check_edges为True时
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            # 这个break的意思是当有一个alien触边，则停止遍历检查是不是还有alien触边，因为已经执行了整行同时下调位置y
            break


# 这个函数放在上个函数的if条件下执行，即当有一个alien触边时，则遍历所有alien使它们全部下调位置(增加y坐标值)
def change_fleet_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    # 整行外星人全部下调位置后，整体向左移动，因此direction的调用是在遍历全部结束后
    ai_setting.fleet_direction *= -1


def update_aliens(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """
    检查是否有外星人到达屏幕边缘
    然后更新所有外星人的位置
    """
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    # 检测外星人是否与飞船发生碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets):
    if stats.ship_left > 0:
        # 飞船数减1
        stats.ship_left -= 1
        # 飞船减少后更新计分牌中显示的剩余飞船数
        sb.prep_ships()
        # 飞船被毁后，需要重置游戏内容，清空子弹和外星人列表，再重新建立外星人
        aliens.empty()
        bullets.empty()
        create_fleets(ai_setting, screen, ship, aliens)
        # 屏幕底部中央重新放置新的飞船
        ship.center_ship()
        # 暂停程序执行，使玩家注意到飞船被撞毁和游戏重置
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, sb, screen, ship, aliens, bullets)
            break
