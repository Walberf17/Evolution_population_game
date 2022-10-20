from variables import *
import random
import math

def set_scene(name , obj):
	SCENES[name] = obj

def calc_proportional_size(expected = None , max_area = None , max_rect = None):
	"""

	:param expected:
	:param max_area:
	:param max_rect:
	:return:
	"""
	if max_rect is None:
		max_rect = screen_rect
	if max_area is None:
		max_area = [1,1]
	max_sizes = pg.Vector2(max_rect.size)
	proportion = max_sizes.elementwise() / max_area
	if expected is None:
		expected = [1 , 1]
	if type(expected) in [float , int]:
		return (proportion[1]*expected)
	elif len(expected) == 2:
		return proportion.elementwise()*expected
	elif len(expected) == 4:
		pos = proportion.elementwise()*expected[:2] + max_rect.topleft
		size = proportion.elementwise()*expected[2:]
		return [pos , size]
	else:
		raise TypeError(f'value not good enought, {expected}')

def get_ang(card1 , card2):
	"""
	calcs the angle from 2 diferent cards
	:param card1: Card object
	:param card2: Card object
	:return: angle in radians
	"""
	x1 , y1 = card1.rect.center
	x2 , y2 = card2.rect.center
	return math.atan2((y2 - y1) , (x2 - x1))

def set_pop_class(pop_class):
	global POPULATION_CLASSES
	POPULATION_CLASSES[0] = pop_class

def create_enemies(Population):
	if len(enemies_group) <= 1:
		if random.random() < .5:
			w = random.uniform(.4 , .8)
			h = random.uniform(.1 , .3)
			x = random.uniform(w/2 , (1-w/2))
			y = -h/screen_rect.height
			pop_size = random.randint(1 , 3)

			Population(pop_size = pop_size , main_group = enemies_ind_groups , main_enemies_group = characters_group , groups = [enemies_group] , movement_speed = (0 , 2) , center = [x , y] , area = [w , h] , age = 9)

def create_filter():
	NewFilter = random.choice(FILTERS_CLASSES)
	posx = random.uniform(.3 , .7)

	val = random.randrange(-5 , 5)
	while val == 0:
		val = random.randrange(-5 , 5)
	NewFilter(val, [posx , -.1])

def set_filter_classes(class_lit):
	global FILTERS_CLASSES
	for c in class_lit:
		FILTERS_CLASSES.append(c)
