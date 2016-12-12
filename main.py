#!/bin/python

###############################################################
## Main.py  -  Initialisation calls & Higher level functions ##
###############################################################

import pyglet
import random

from shooter import config
from shooter import file_watcher
from shooter import obj		#Object module	-Severok
from shooter import proc	#Processing related functions
from shooter import splash_screen
from math import atan2,atan, sin, cos, degrees, pi, sqrt


Game_WIDTH = 640
Game_HEIGHT = 480

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

game = Game_Window()


window = pyglet.window.Window(fullscreen = True)
print(window.height/Game_HEIGHT)
print(window.width/Game_WIDTH)
input_handle = proc.InputHandler(window)

# color_tuple is a four-colour tuple (R, G, B, A).
def create_color(width, height, color_tuple):
    img = pyglet.image.SolidColorImagePattern(color_tuple).create_image(32, 32)
    sprite = pyglet.sprite.Sprite(img)
    return sprite

def create_image(image_filename):
    img = pyglet.image.load(image_filename)
    sprite = pyglet.sprite.Sprite(img)
    return sprite

def show_dg_splash():
    splash = obj.spawn('Misc', "DG Splash", 0, 0, splash_screen.SplashScreen)
    splash.on_death = lambda: start_game()
    misc_list.append(splash)

def start_game():
    for obj_list in main_list:
        obj_list[:] = []

    background = obj.spawn('Misc', 'Background', 0, 0)
    backgrounds_list.append(background)

    CRATER_WIDTH = 128
    CRATER_HEIGHT = 64

    num_craters = random.randrange(3) + 2
    for i in range(num_craters):
        c = obj.spawn("Misc", "Crater", random.randrange(WINDOW_WIDTH - CRATER_WIDTH), random.randrange(WINDOW_HEIGHT - CRATER_HEIGHT))        
        c.size = 0.5 if random.randrange(100) <= 75 else 1
        backgrounds_list.append(c)

    player = obj.spawn('Player', "Player_Basic", window.width / 2, window.height / 2)
    player.on_death = lambda: game_over()
    player_list.append(player)

    pyglet.clock.schedule_interval(spawn_random, 1)

def game_over():
    over = obj.spawn("Misc", "Game Over", 0, 0)
    over.x = (window.width - over.img.width) / 2
    over.y = (window.height - over.img.height) / 2
    over.on_death = lambda: start_game()
    misc_list.append(over)

def frame_callback(dt):

    #Check user input
    proc.input(main_list,input_handle)    

    proc.ai(enemy_list,main_list)			#Make decision for movement/attack

    proc.ai(bullet_list,main_list)

    proc.ai(misc_list,main_list)              #Misc objects intended as cosmetic. No need to check collisions at this time.

    proc.update(main_list)
    for player in player_list:                 			#If player reaches boundry of screen
        if player.x > window.width-100: player.x = window.width-100#Push them back by previous movement.
        if player.x < 100: player.x = 100
        if player.y > window.height-100: player.y = window.height - 100
        if player.y < 100: player.y = 100
    
    proc.collision(main_list)

def spawn_random(dt):
    type_select = random.randrange(3)
    side = random.randrange(4)
    rand_x = random.randrange(WINDOW_WIDTH)
    rand_y = random.randrange(WINDOW_HEIGHT)

    type_select_result = {
        0: "Enemy_Basic",
        1: "Enemy_Coward",
        2: "Enemy_Slow"
    }

    position_generate_x = {
        0: WINDOW_WIDTH + 100,
        1: -100,
        2: rand_x,
        3: rand_x
    }

    position_generate_y = {
        0: rand_y,
        1: rand_y,
        2: -100,
        3: WINDOW_HEIGHT + 100
    }

    spawn_enemy(type_select_result[type_select], position_generate_x[side],position_generate_y[side])
  
def spawn_enemy(id, x, y):
    e = obj.spawn("Enemy", id, x, y)
    enemy_list.append(e)
    return e


Object_handler = obj.Object_handler()
Screen_handler = proc.Screen()


file_watcher.watch('data/object.json', obj.load_prototype_data)

if config.get("skip_splash_screens") != True:
    dg_splash_screen = obj.spawn('Misc', "MG Splash", 0, 0, splash_screen.SplashScreen)
    dg_splash_screen.on_death = lambda: show_dg_splash()
    misc_list.append(dg_splash_screen)
else:
    start_game()

obj.GameObject.note_screen_size(WINDOW_WIDTH, WINDOW_HEIGHT)

