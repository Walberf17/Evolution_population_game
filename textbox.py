"""

"""
# from variables_and_definitions import *
from definitions import *
from variables import *
import pygame as pg
from pygame.sprite import Sprite

# Some Default Font


class TextBox(Sprite):
	""" this will work with long sentences,
	cutinh then is smaller ones , and drawing
	each on screen.
	param txt : string
	param rect : pg.Rect
	param font : pg.font.SysFont
	param font_color : pg.color
	param bg_color : pg.color
	"""

	def __init__(self , text , rect , rect_to_be, centered_x = True , centered_y = False, font = None ,
	             font_color = "white" , bg_color = "black" , groups = None):
		"""
		It takes a string, a pg.Rect , a pg.font,
		font color and a background color.

		:param text : string
		:param centered_x: if the prefix should be centered in the x axis
		:param rect : pg.Rect
		:param font : pg.font.SysFont
		:param font_color : pg.color
		:param bg_color : pg.color
		"""
		if groups is None:
			groups = []
		if type(groups) not in [set , list , tuple]:
			groups = list(groups)
		super().__init__(*groups)
		self.divisor = 20
		if font is None:
			font_size = int(screen_rect.w / self.divisor)
			font = pg.font.SysFont("arial" , font_size , False , False)
		self.text = text
		self.divisor = 20
		self.font = font
		self.font_color = font_color
		self.bg_color = bg_color
		self.rect = pg.Rect(calc_proportional_size(expected = rect , max_area = [1,1] , max_rect = rect_to_be))
		self.centered_x = centered_x
		self.centered_y = centered_y
		if centered_x:
			self.rect.centerx = rect_to_be.centerx
		if centered_y:
			self.rect.centery = rect_to_be.centery
		self.max_size = self.rect.w*0.9
		self.line_w , self.line_h = self.font.size(str(text))
		self.lines = []
		self.cliked = False

	def draw(self, screen_to_draw):
		"""
		Draw the prefix box in the given surface.
		:param screen_to_draw: pg.Surface Object
		:return: None
		"""
		txt = self.font.render(self.text , True , self.font_color , self.bg_color)
		txt_rect = txt.get_rect()
		txt_rect.center = self.rect.center
		screen_to_draw.blit(txt , txt_rect)

	def update_text(self , new_text):
		self.text = new_text
