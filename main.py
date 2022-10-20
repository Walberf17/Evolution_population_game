
from definitions import *
from scenes import Scene
from player_classes import Population
import pygame as pg
from timer import Timer
from functools import partial
from filters import HPFilter, RangeFilter, AgilityFilter, StrengthFilter, AgeFilter , PopFilter

set_filter_classes([AgilityFilter])
# set_filter_classes([HPFilter, RangeFilter, AgilityFilter, StrengthFilter, AgeFilter , PopFilter])

pg.init()

main_game = Scene(screen_to_draw = screen , dicts_to_do = main_scene_dict)

main_player = Population(children_image = 2 , children_dict = dict_with_images , pop_size = 10 ,
                         main_group = characters_group , main_enemies_group = enemies_ind_groups ,
                         groups = [players_group] , center = [.5 , .5] , area = [1 , .8] , age = 0)

Timer(time_var = 1 , recurrent = True , command = partial(create_enemies , (Population)) , groups = [timers])

Timer(time_var = 20 , recurrent = True , command = partial(create_filter) , groups = [timers])


main_game.run()