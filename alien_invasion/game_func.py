import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	'''响应飞船被撞'''
	if stats.ship_left > 0:
		stats.ship_left -= 1
	
		#清空
		aliens.empty()
		bullets.empty()
	
		#新建外星人，重置飞船
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		#暂停
		sleep(2)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
def check_event_down(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets): 
	#创建子弹并加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allow:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def check_event_up(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False
		
def check_events(ai_settings, screen, stats, play_button, ship,aliens,
		bullets):
	'''响应按键和鼠标事件'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			check_event_down(event, ai_settings, screen, ship, bullets)
		
		elif event.type == pygame.KEYUP:
			check_event_up(event, ship)	
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
				bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
		bullets, mouse_x, mouse_y):
	button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_click and not stats.game_active:
		#重置游戏设置
		ai_settings.initialize_dynamic_settings()
		#隐藏光标
		pygame.mouse.set_visible(False)
		#重置游戏数据
		stats.reset_stats()
		stats.game_active = True
		
		#清空外星人和子弹
		aliens.empty()
		bullets.empty()
		
		creat_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
			
def update_screen(ai_settings, screen, stats, ship, aliens, bullets,
		play_button):
	'''更新屏幕'''
	#重新绘制
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	if not stats.game_active:
		play_button.draw_button()
	
	#可见
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, ship, aliens, bullets):
	'''更新子弹位置，并删除已消失子弹'''
	bullets.update()
	#删除消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)
	
def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
	'''检查是否有子弹击中，若有删除两者'''
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if len(aliens) == 0:
		#删除现有子弹，新建外星人
		bullets.empty()
		ai_settings.increase_speed()
		creat_fleet(ai_settings, screen, ship, aliens)
		
def get_number_alien_x(ai_settings, alien_width):
	'''计算一行容纳量'''
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_alien_x = int(available_space_x / (2 * alien_width))
	return number_alien_x

def get_number_rows(ai_settings, ship_height, alien_height):
	'''计算屏幕可容纳多少行外星人'''
	available_space_y = (ai_settings.screen_height - 
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
	'''创建一个外星人放在当前行'''
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
			
def creat_fleet(ai_settings, screen, ship, aliens):
	'''创建外星人群'''
	#创建一个外星人，并计算每行容纳量
	alien = Alien(ai_settings, screen)
	number_alien_x = get_number_alien_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)
	
	#创建外星人群
	for row_number in range(number_rows):
		for alien_number in range(number_alien_x):
			creat_alien(ai_settings, screen, aliens, alien_number, row_number)
	
def check_fleet_edge(ai_settings, aliens):
	'''有外星人到达边缘是采取相应措施'''
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	'''整群外星人下移并改变方向'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	'''检查边缘并更新所有外星人位置'''
	check_fleet_edge(ai_settings, aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
	check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets)