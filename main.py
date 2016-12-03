#!/bin/python

import pyglet
import copy	#Used to copy object prototypes to spawn active objects.
import obj	#Object module	-Severok
import ai	#AI	module	-Severok

player_list = []	#List of objects in active play.
enemy_list = []			#List of object prototypes in obj.py
bullet_list = []
misc_list = []


window = pyglet.window.Window()

obj.init_obj()


#img = pyglet.image.load('images/splash-mg.png')
#sprite = pyglet.sprite.Sprite(img, x = (window.width - img.width) // 2,
#    y = (window.height - img.height) // 2)
#objectlist.append sprite

@window.event
def on_mouse_motion(x,y,dx,dy):
    pass

@window.event
def on_draw():
    window.clear()
    for player in player_list:		#Render player sprite
        player.sprite.draw()
    for enemy in enemy_list:		#Render enemy sprites
        enemy.sprite.draw()
    for bullet in bullet_list:		#Render bullet sprites
        bullet.sprite.draw()
    for misc in misc_list:		#Render Misc sprites
        misc.sprite.draw()


#obj.spawn(misc_list,'misc',1,0,0)
	#Initialisation
obj.spawn(player_list,'player',0,(window.width)/2, (window.height)/2)
obj.spawn(enemy_list,'enemy',0,100,100)
obj.spawn(enemy_list,'enemy',1,200,200)

pyglet.app.run()
