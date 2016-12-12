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

def start_game():
    obj.Player_list[:]=[]
    obj.Enemy_list[:]=[]
    obj.Bullet_list[:]=[]
    obj.Misc_list[:]=[]
    obj.Backgrounds_list[:]=[]

    #background = Object_handler.spawn('Misc', 'Background', 0, 0)

    CRATER_WIDTH = 128
    CRATER_HEIGHT = 64

    # 2-4 craters
    num_craters = random.randrange(3) + 2
    for i in range(num_craters):
        c = Object_handler.spawn("Misc", "Crater", random.randrange(Screen_handler.window.width - CRATER_WIDTH), random.randrange(Screen_handler.window.height - CRATER_HEIGHT))        
        c.size = 0.5 if random.randrange(100) <= 75 else 1 # mostly small craters
        obj.Backgrounds_list.append(c)

    player = Object_handler.spawn('Player', "Player_Basic", Screen_handler.window.width / 2, Screen_handler.window.height / 2)
    player.on_death = lambda: game_over()

    pyglet.clock.schedule_interval(Object_handler.spawn_random, 1)

def game_over():
    over = Object_handler.spawn("Misc", "Game Over", 0, 0)
    over.x = (Screen_handler.window.width - over.img.width) / 2
    over.y = (Screen_handler.window.height - over.img.height) / 2
    over.on_death = lambda: start_game()

def frame_callback(dt):

    #Check user input
    Screen_handler.input()
    Object_handler.update()

    for player in obj.Player_list:                 			#If player reaches boundry of screen
        # TODO: consider replacing with walls that border the map (perhaps off-screen ones)
        if player.x > Screen_handler.window.width - 100:
            player.x = Screen_handler.window.width - 100    #Push them back by previous movement.
        if player.x < 100:
            player.x = 100
        if player.y > Screen_handler.window.height - 100:
            player.y = Screen_handler.window.height - 100
        if player.y < 100:
            player.y = 100


Object_handler = obj.Object_handler()
Screen_handler = proc.Screen()

file_watcher.watch('data/object.json', obj.load_prototype_data)

if config.get("skip_splash_screens") != True:
    dg_splash_screen = Object_handler.spawn('Misc', "MG Splash", 0, 0, splash_screen.SplashScreen)
    dg_splash_screen.on_death = lambda: show_dg_splash()
else:
    start_game()

pyglet.clock.schedule(frame_callback)
pyglet.clock.schedule_interval(frame_callback, 1 / 30.0) # call frame_callback at 30FPS

pyglet.app.run()

