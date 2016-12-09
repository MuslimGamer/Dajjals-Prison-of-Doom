#!/bin/python

import pyglet
import random

from shooter.config import Config
from shooter import file_watcher
from shooter import obj		#Object module	-Severok
from shooter import proc	#Processing related functions
from shooter import splash_screen

window = pyglet.window.Window()
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
    player = obj.spawn('Player', "Basic", window.width / 2, window.height / 2)
    player.on_death = lambda: start_game()
    player_list.append(player)

    pyglet.clock.schedule_interval(spawn_random, 1)

def frame_callback(dt):
    #Clear collision matrix

    #Check user input
    #Update player position 
    proc.input(main_list,input_handle)

    proc.update(player_list)

    proc.ai(enemy_list,main_list)			#Make decision for movement/attack
    proc.update(enemy_list)
    #proc.collision(enemy_list)		#Check if enemy overlap with player
    
    proc.ai(bullet_list,main_list)
    proc.update(bullet_list)		#Progress Bullet position
    #proc.collision(bullet_list)		#Scan for collision with other objects.

    proc.ai(misc_list,main_list)              #Misc objects intended as cosmetic. No need to check collisions at this time.
    proc.update(misc_list)
    
    proc.collision(main_list)

def spawn_random(dt):
    type_select = random.randrange(3)
    side = random.randrange(4)
    rand_x = random.randrange(640)
    rand_y = random.randrange(480)

    type_select_result = {
        0: "Basic",
        1: "Coward",
        2: "Slow"
    }

    position_generate_x = {
        0: 740,
        1: -100,
        2: rand_x,
        3: rand_x
    }

    position_generate_y = {
        0: rand_y,
        1: rand_y,
        2: -100,
        3: 580
    }

    spawn_enemy(type_select_result[type_select], position_generate_x[side],position_generate_y[side])
  
def spawn_enemy(id, x, y):
    e = obj.spawn("Enemy", id, x, y)
    enemy_list.append(e)
    return e

@window.event
def on_mouse_press(x, y, button, modifiers):
    input_handle.mouse_pressed(x,y,button)

@window.event
def on_mouse_release(x,y,button, modifiers):
    input_handle.mouse_released(button)
    #Todo - Load variables into handler for passing into proc.py input function. 
    #       Migrate code below into function with keyboard processing.

@window.event
def on_mouse_drag(x,y,dx,dy, buttons, modifiers):
    input_handle.mouse_dragged(x, y)

@window.event
def on_draw():				#Kept seperate from processing callback, Frame rate not tied to simulation speed.
    window.clear()
    for player in player_list:		#Render player sprite
        player.sprite.draw()
    for enemy in enemy_list:		#Render enemy sprites
        enemy.sprite.draw()
    for bullet in bullet_list:		#Render bullet sprites
        bullet.sprite.draw()
    for misc in misc_list:		#Render Misc sprites
        misc.sprite.draw()

@window.event
def on_close():
    file_watcher.stop()

main_list = []
player_list = []		#List of objects in active play.
enemy_list = []			#List of object prototypes in obj.py
bullet_list = []
misc_list = []

main_list.append(player_list)
main_list.append(enemy_list)
main_list.append(bullet_list)
main_list.append(misc_list)

file_watcher.watch('data/object.json', obj.load_prototype_data)
file_watcher.watch('data/config.json', lambda raw_json: Config.instance.load(raw_json))

dg_splash_screen = obj.spawn('Misc', "MG Splash", 0, 0, splash_screen.SplashScreen)
dg_splash_screen.on_death = lambda: show_dg_splash()
misc_list.append(dg_splash_screen)

pyglet.clock.schedule(frame_callback)
pyglet.clock.schedule_interval(frame_callback, 1 / 30.0) # call frame_callback at 30FPS

pyglet.app.run()

