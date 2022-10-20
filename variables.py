import pygame as pg

######## Initialize pygame
pg.init()
pg.font.init()

######## Create main screen
screen = pg.display.set_mode((800 , 1000))
screen_rect = screen.get_rect()
creation_rect = pg.Rect(0 , 0 , screen_rect.width , 300)
creation_rect.midbottom = screen_rect.midtop
FPS = 30
REPULTION_FORCE = .8
POPULATION_CLASSES = [None]
FILTERS_CLASSES = []

######## Groups
text_boxes_group = pg.sprite.Group()

# the player groups
players_group = pg.sprite.Group()
characters_group = pg.sprite.Group()

# the enemies groups
enemies_group = pg.sprite.Group()
enemies_ind_groups = pg.sprite.Group()


buttons_group = pg.sprite.Group()
shoots_group = pg.sprite.Group()
filter_group = pg.sprite.Group()

moving_objects_group = set()

timers = []

######## Variables
FORCE_TO_CARDS = 2
CARD_SIZE = [screen_rect.w * 0.15 , screen_rect.h * .15]
BATTLE_DECK = [5, 5 , 5]

######## Fonts for texts
font_size = int(screen_rect.h * .1)
main_menu_font = pg.font.SysFont("Arial" , font_size , False , True)

######## Sets of things
SCENES = {"Main Menu": None ,
          "Main Adventure": None ,
          "Main Battle": None ,
          "Items Menu": None ,
          "Abilities Menu": None ,
          "Testes": None}

# for images in general
IMAGES_PATH = 'Images'

dict_with_images = {
	'path' : 'SpaceShip',
	1:{
		"adress": '1.png',
	},
	2:{
		'adress': '2.png',
		'size': [64,64]
	}
}

######## dicts and lists

exemple_dict = {
		'update': [],
		'move': [],
		'draw': [],
		'click_down': [],
		'click_up': [],
		'key_down': [],
		'key_up': [],
		'multi_gesture': [],
		'finger_down': [],
		'finger_up': [],
		'finger_motion' : []
		}

main_scene_dict = {
		'update': [players_group , enemies_group , timers , filter_group , shoots_group ],
		'move': [players_group , enemies_group , filter_group , shoots_group],
		'draw': [filter_group , players_group , enemies_group , shoots_group],
		'click_down': [players_group],
		'click_up': [],
		'key_down': [players_group],
		'key_up': [players_group],
		'multi_gesture': [],
		'finger_down': [],
		'finger_up': [],
		'finger_motion' : []
		}

