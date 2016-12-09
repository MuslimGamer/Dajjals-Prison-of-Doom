#!/bin/python

import pyglet
import random

from shooter import config
from shooter import file_watcher
from shooter import obj		#Object module	-Severok
from shooter import proc	#Processing related functions
from shooter import splash_screen

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
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

    player = obj.spawn('Player', "Basic", window.width / 2, window.height / 2)
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
    rand_x = random.randrange(WINDOW_WIDTH)
    rand_y = random.randrange(WINDOW_HEIGHT)

    type_select_result = {
        0: "Basic",
        1: "Coward",
        2: "Slow"
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

    for bg in backgrounds_list:
        bg.sprite.draw()
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

main_list = [] # TODO: convert to a hash or a class
player_list = []		#List of objects in active play.
enemy_list = []			#List of object prototypes in obj.py
bullet_list = []
misc_list = []
backgrounds_list = []   # Stuff that makes up our background

# We keep things in a specific order. This is fragile, but okay for now.
main_list.append(player_list)
main_list.append(enemy_list)
main_list.append(bullet_list)
main_list.append(misc_list)
main_list.append(backgrounds_list)

file_watcher.watch('data/object.json', obj.load_prototype_data)

if config.get("skip_splash_screens") != True:
    dg_splash_screen = obj.spawn('Misc', "MG Splash", 0, 0, splash_screen.SplashScreen)
    dg_splash_screen.on_death = lambda: show_dg_splash()
    misc_list.append(dg_splash_screen)
else:
    start_game()

obj.GameObject.note_screen_size(WINDOW_WIDTH, WINDOW_HEIGHT)

pyglet.clock.schedule(frame_callback)
pyglet.clock.schedule_interval(frame_callback, 1 / 30.0) # call frame_callback at 30FPS

pyglet.app.run()

