#!/bin/python

###############################################################
## Main.py  -  Initialisation calls & Higher level functions ##
###############################################################

import pyglet
import random
import os
import sys

# Support for PyInstaller --onefile. It creates an archive exe that
# unpacks to a temp directory. We need to convince all our file I/O
# to use that directoy as the application base dir. chdir is the
# easiest way, if we use relative paths for everything else.
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

from shooter import config
from shooter import file_watcher
from shooter import obj		#Object module	-Severok
from shooter import sound
from shooter.player import Player



from shooter import proc	#Processing related functions
from shooter import splash_screen
from math import atan2,atan, sin, cos, degrees, pi, sqrt

GAME_WIDTH = 1024
GAME_HEIGHT = 576

obj.GAME_WIDTH = GAME_WIDTH
obj.GAME_HEIGHT = GAME_HEIGHT

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
    splash = Object_handler.spawn("Misc", "DG Splash", 192, 48, splash_screen.SplashScreen)
    center(splash)
    splash.on_death = lambda: start_game()

def center(game_obj):
    game_obj.x = (Screen_handler.width - game_obj.img.width) / 2
    game_obj.y = (Screen_handler.height - game_obj.img.height) / 2

def start_game():
    # Clear everything on screen
    obj.Player_list[:]=[]
    obj.Enemy_list[:]=[]
    obj.Bullet_list[:]=[]
    obj.Misc_list[:]=[]
    obj.Pickup_list[:]=[]
    obj.Backgrounds_list[:]=[]

    background = Object_handler.spawn('Background', 'Background', 0, 0)

    CRATER_WIDTH = 128
    CRATER_HEIGHT = 64

    # 2-4 craters
    num_craters = random.randrange(3) + 2
    for i in range(num_craters):
        c = Object_handler.spawn("Background", "Crater", random.randrange(Screen_handler.width - CRATER_WIDTH), random.randrange(Screen_handler.height - CRATER_HEIGHT))        
        c.size = 0.5 if random.randrange(100) <= 75 else 1 # mostly small craters
        obj.Backgrounds_list.append(c)

    player = Object_handler.spawn('Player', "Player_Basic", Screen_handler.width / 2, Screen_handler.height / 2, Player)
    player.on_death = lambda: game_over()

    pyglet.clock.schedule_interval(Object_handler.spawn_random, 1)

    Screen_handler.draw_ui = True

def game_over():
    over = Object_handler.spawn("Misc", "Game Over", 0, 0)
    center(over)
    print("Over and out: {0}, {1}".format(over.x, over.y))
    pyglet.clock.unschedule(Object_handler.spawn_random)

    over.on_death = lambda: start_game()

def frame_callback(dt):
    #Check user input
    Screen_handler.input()
    Object_handler.update()
    sound.SoundHandler.play()

    for player in obj.Player_list:                 			#If player reaches boundry of screen
        # TODO: consider replacing with walls that border the map (perhaps off-screen ones)
        if player.x > Screen_handler.width - player.img.width:
            player.x = Screen_handler.width - player.img.width    #Push them back by previous movement.
        if player.x < 0:
            player.x = 0
        if player.y > Screen_handler.height - player.img.height:
            player.y = Screen_handler.height - player.img.height
        if player.y < 0:
            player.y = 0
    
Object_handler = obj.Object_handler()
Screen_handler = proc.Screen(GAME_WIDTH, GAME_HEIGHT)

file_watcher.watch('data/object.json', obj.load_prototype_data)

if config.get("skip_splash_screens") != True:
    screen = Object_handler.spawn('Misc', "MG Splash", 0, 0, splash_screen.SplashScreen)
    center(screen)
    screen.on_death = lambda: show_dg_splash()
else:
    start_game()

pyglet.clock.schedule(frame_callback)
pyglet.clock.schedule_interval(frame_callback, 1 / 30.0) # call frame_callback at 30FPS


# Shut down threads cleanly in case of a crash
try:
    pyglet.app.run()
except:
    file_watcher.stop()
    raise

