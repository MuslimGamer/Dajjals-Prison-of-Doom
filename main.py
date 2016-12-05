#!/bin/python

import pyglet
import copy	#Used to copy object prototypes to spawn active objects.
import obj	#Object module	-Severok
import proc	#Processing related functions

player_list = []	#List of objects in active play.
enemy_list = []			#List of object prototypes in obj.py
bullet_list = []
misc_list = []

window = pyglet.window.Window()

obj.init_obj()
#collision_map[window.width][window.height]

#img = pyglet.image.load('images/splash-mg.png')
#sprite = pyglet.sprite.Sprite(img, x = (window.width - img.width) // 2,
#    y = (window.height - img.height) // 2)
#objectlist.append sprite

@window.event
def on_mouse_motion(x,y,dx,dy):
    pass

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

def frame_callback(dt):
    #Clear collision matrix

    #Check user input
    #Update player position 

    proc.input(player_list)
    proc.update(player_list)
    proc.collision(player_list)

    proc.ai(enemy_list)			#Make decision for movement/attack
    proc.update(enemy_list)
    proc.collision(enemy_list)		#Check if enemy overlap with player
			
    proc.update(bullet_list)		#Progress Bullet position
    proc.collision(bullet_list)		#Scan for collision with other objects.

    proc.ai(misc_list)
    proc.update(misc_list)
					#Misc objects intended as cosmetic. No need to check collisions at this time.

def splash(dt):
    for item in misc_list:
        misc_list.remove(item)
    obj.spawn(player_list,'Player',0,(window.width)/2, (window.height)/2)
    obj.spawn(enemy_list,'Enemy',0,100,100)
    obj.spawn(enemy_list,'Enemy',1,200,200)
    pyglet.clock.schedule(frame_callback)
    pyglet.clock.schedule_interval(frame_callback, 1/30)

obj.spawn(misc_list,'Misc',0,0,0)
pyglet.clock.schedule_once(splash, 1)

pyglet.app.run()