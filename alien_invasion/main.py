import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
import game_func as gf


def run_game():
    # 初始化游戏和屏幕
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # 创建Play按钮
    play_button = Button(ai_settings, screen, 'Play')
    # 创建用于存储统计信息的实例
    stats = GameStats(ai_settings)
    # 创建飞船
    ship = Ship(screen, ai_settings)
    # 创建存储子弹的编组
    bullets = Group()
    # 创建外星人的编组
    aliens = Group()   
    # 创建外星人群
    gf.creat_fleet(ai_settings, screen, ship, aliens)  
    # 开始游戏循环
    while True:
        # 监视事件
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, 
bullets)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, 
        play_button)

run_game()