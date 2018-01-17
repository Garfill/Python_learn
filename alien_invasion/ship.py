import pygame

from settings import Settings

class Ship():

	def __init__(self, screen, ai_settings):
		'''初始化飞船位置'''
		self.screen = screen
		self.ai_settings = ai_settings
	
		#加载飞船
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
	
		#飞船居中
		self.rect.centerx = self.screen_rect.centerx
		self.rect.centery = self.screen_rect.bottom
		
		# center中存储小数
		self.center = float(self.rect.centerx)
		
		# 移动标志
		self.moving_right = False
		self.moving_left = False
		
	def update(self):
		"""根据移动标志调整飞船的位置"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		
		self.rect.centerx = self.center
	
	def blitme(self):
		'''绘制飞船'''
		self.screen.blit(self.image, self.rect)
		
	def center_ship(self):
		self.center = self.screen_rect.centerx