class Settings():
	'''存储设置'''
	def __init__(self):
		'''初始化游戏设置'''
		# 屏幕设置
		self.screen_width = 600
		self.screen_height = 600
		self.bg_color = (230,230,230)
		
		#飞船设置
		self.ship_limit = 2
		
		#子弹设置
		self.bullet_width = 4
		self.bullet_height = 10
		self.bullet_color = 60, 60, 60
		self.bullets_allow = 4
		
		#外星人设置
		self.fleet_drop_speed = 10
		
		
		#加快节奏
		self.speedup_scale = 1.1 
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		'''初始化随着游戏的变化'''
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 1
		self.alien_speed_factor = 0.5
		
		#fleet_derection为1表示右移，为-1表示左
		self.fleet_direction = 1	
		
	def increase_speed(self):
		'''提高速度'''
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor  *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale