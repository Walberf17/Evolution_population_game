"""
this works with the possible FILTERS_CLASSES,
such as:
	aging
	getting younger
	evolving
	reproducing
	death
	hunger
	increase stats
	decrease stats

"""

# import things
import math
import random
from definitions import *
from animations import Animations
from functools import partial
from textbox import TextBox as TB
from pygame.sprite import Group

default_area = (.3 , .01)

negative_sign = ''
neutral_sign = '+'



class Filter(Animations):
	"""
	Main class of the Filters to use
	"""
	def __init__(self , movement_speed = (0,0) , command = None , image_name = None , area = (.3 , .1) ,
	             dict_with_images = None , rect_to_be = None , center = None , relative_pos = None , color = "blue" ,
	             groups = None , prefix = '' , value = 0.):
		Animations.__init__(self , image_name = image_name , area = area ,
		                    dict_with_images = dict_with_images , rect_to_be = rect_to_be ,
		                    center = center , relative_pos = relative_pos , color = color , groups = groups)

		self.movement_speed = pg.Vector2(movement_speed)
		self.value = value
		self.prefix = prefix
		text = f'{self.prefix} {self.get_sign()} {self.value}'
		self.tb = TB(text , rect = (0, 0, .1 , .5) , rect_to_be = self.rect , centered_x = True , centered_y = True)

	def command(self , **kwargs):
		return

	def move(self):
		self.rect.move_ip(self.movement_speed)

	def update(self):
		Animations.update(self)

		self.check_kill()

		self.tb.rect.center = self.rect.center
		for player in characters_group:
			if player.rect.colliderect(self.rect):
				self.command()
				if not self.change_state('death'):
					self.kill()

	def check_kill(self):
		if self.rect.collidelist([screen_rect , creation_rect]) == -1:
			self.kill()


	def draw(self , screen_to_draw):
		Animations.draw(self , screen_to_draw = screen_to_draw)
		self.tb.draw(screen_to_draw)

	def get_sign(self , value = None):
		if value is None:
			value = self.value

		if value < 0:
			sign = negative_sign
		else:
			sign = neutral_sign
		return sign


class CountingFilter(Filter):
	def __init__(self , command = None, value = 1, prefix = '' , **kwargs):
		Filter.__init__(self , value = value , command = command , prefix = prefix , **kwargs)
		self.collided_things = set()
		self.per_click_value = int(value/abs(value))
		self.prefix = prefix
		self.times_to_collide = abs(value)
		new_text = f'{self.prefix} {self.get_sign()}{self.per_click_value} x {self.times_to_collide}'
		self.tb.update_text(new_text = new_text)


	def update(self):
		Animations.update(self)

		self.check_kill()

		self.tb.rect.center = self.rect.center
		if self.times_to_collide >= 1:
			for player in characters_group:
				if self.times_to_collide < 1:
					break
				if player.rect.colliderect(self.rect):

					if player not in self.collided_things:

						self.times_to_collide -= 1

						self.update_text()

						self.command(player)
						self.collided_things.add(player)
						if self.times_to_collide < 1:
							break

		elif not self.change_state('death'):
			self.kill()

	def update_text(self):
		new_text = f'{self.prefix} {self.get_sign()}{self.per_click_value} x {self.times_to_collide}'
		self.tb.update_text(new_text = new_text)






class HPFilter(Filter):
	def __init__(self , value , center):
		Filter.__init__(self , prefix = f'HP' , movement_speed = (0, 1) , image_name = None , area =default_area ,
		                dict_with_images = None , rect_to_be = screen_rect , center = center ,relative_pos = None ,
		                color = "red" , groups =  [filter_group] , value = value)

	def command(self):
		for player in players_group:
			player.update_hp(self.value)


class RangeFilter(Filter):
	def __init__(self , value , center):
		Filter.__init__(self , prefix = f'Range' , movement_speed = (0, 1) , image_name = None , area = default_area ,
		                dict_with_images = None , rect_to_be = screen_rect , center = center , relative_pos = None ,
		                color = "yellow" , groups =  [filter_group] , value = value)

	def command(self):
		for player in players_group:
			player.update_range(self.value)


class AgilityFilter(CountingFilter):
	def __init__(self , value , center):
		CountingFilter.__init__(self , prefix = f'Agi' , movement_speed = (0, 1) , image_name = None ,
		                        area = default_area , dict_with_images = None , rect_to_be = screen_rect ,
		                        center = center , relative_pos = None , color = "green" , groups = [filter_group] ,
		                        value = value)

	def command(self , character = None):
		character.update_agility(self.value)


class StrengthFilter(Filter):
	def __init__(self , value , center):

		Filter.__init__(self , prefix = f'Str' , movement_speed = (0, 1) , image_name = None , area = default_area ,
		                dict_with_images = None , rect_to_be = screen_rect , center = center , relative_pos = None ,
		                color = "black" , groups =  [filter_group] , value = value)

	def command(self):
		for player in players_group:
			player.update_strength(self.value)


class AgeFilter(Filter):
	def __init__(self , value , center):
		Filter.__init__(self , prefix = f'Age' , movement_speed = (0, 1) , image_name = None , area = default_area ,
		                dict_with_images = None , rect_to_be = screen_rect , center = center , relative_pos = None ,
		                color = "white" , groups =  [filter_group] , value = value)

	def command(self):
		for player in players_group:
			player.update_age(self.value)


class PopFilter(CountingFilter):
	def __init__(self , value , center):
		CountingFilter.__init__(self , prefix = f'Pop' , movement_speed = (0, 1) , image_name = None ,
		                        area = default_area , dict_with_images = None , rect_to_be = screen_rect ,
		                        center = center , relative_pos = None , color = "gray" , groups =  [filter_group] ,
		                        value = value)

	def command(self , character = None):
		if self.value > 0:
			self.reproduce(character)

		else:
			self.kill_character(character)

	def kill_character(self , character):
		character.kill()

	def reproduce(self , character):
		character.reproduce(self.per_click_value)