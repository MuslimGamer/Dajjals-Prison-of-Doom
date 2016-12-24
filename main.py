#!/bin/python

###############################################################
## Main.py  -  Initialisation calls & Higher level functions ##
###############################################################

import random
import os
import sys
from math import atan2,atan, sin, cos, degrees, pi, sqrt

import pyglet

from shooter import sound

# Support for PyInstaller --onefile. It creates an archive exe that
# unpacks to a temp directory. We need to convince all our file I/O
# to use that directoy as the application base dir. chdir is the
# easiest way, if we use relative paths for everything else.
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

from shooter import config
from shooter import file_watcher

from shooter import sound
from shooter.player import Player
from shooter import obj		#Object module	-Severok

from shooter import proc	#Processing related functions
from shooter import splash_screen
from shooter import ui_manager


GAME_WIDTH = 1024
GAME_HEIGHT = 576

obj.GAME_WIDTH = GAME_WIDTH
obj.GAME_HEIGHT = GAME_HEIGHT

def show_dg_splash():
    splash = Object_handler.spawn("Misc", "DG Splash", 192, 48, splash_screen.SplashScreen)
    center(splash)
    splash.on_death = lambda: start_game()

def center(game_obj):
    game_obj.x = (Screen_handler.width - game_obj.img.width) / 2
    game_obj.y = (Screen_handler.height - game_obj.img.height) / 2

def start_game():
    # Clear everything on screen
    Object_handler.start()
    Screen_handler.score_label = None
    obj.score = 0

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
    
    # TODO: encapsulate
    Screen_handler.score_label = pyglet.text.Label("Final Score: {0}".format(obj.score), font_name = ui_manager.UiManager.FONT_NAME, 
        x = over.x + 160, y = over.y - 32, font_size = 24)

    pyglet.clock.unschedule(Object_handler.spawn_random)

    over.on_death = lambda: start_game()

def frame_callback(dt):
    #Check user input
    Screen_handler.input()
    if not Screen_handler.paused:
        Object_handler.update()
    #sound.SoundHandler.play()

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

