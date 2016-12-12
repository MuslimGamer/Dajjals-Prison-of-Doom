##################################################################
## Proc.py - Processing functions     				##
##################################################################
## Functions relating to Rendering, Input and related functions ##
##################################################################

import pyglet
import random


from pyglet.window import key, mouse
from shooter import obj
from shooter import config

from math import atan2,atan, sin, cos, degrees, pi, sqrt

class Screen:			#Class handling window and window related functions (Draw, Events, Input)
    def __init__(self)
        self.window = pyglet.window.Window(fullscreen = True)
        input_handle = InputHandler(self.window)


    def input(player_list): 
        for player in player_list:
            player.mx = self.input_handle.keyboard[key.A] * -1 + self.input_handle.keyboard[key.D] * 1
            player.my = self.input_handle.keyboard[key.S] * -1 + self.input_handle.keyboard[key.W] * 1

            if not (abs(player.mx) + abs(player.my) == 1):
            # If both keys are down, don't move at 1.4x; move at ~sqrt(2)/2
                player.mx = player.mx * 0.707
                player.my = player.my * 0.707

            if not (player.cooldown):
                if (self.input_handle.is_pressed(mouse.LEFT)):
                    if config.get('melee_enabled'):
                        player.attack("Bullet_Melee",self.input_handle.mouse_x,self.input_handle.mouse_y)
                    else:
                        player.attack("Bullet_Basic",self.input_handle.mouse_x,self.input_handle.mouse_y) 
                elif (self.input_handle.is_pressed(mouse.RIGHT)):
                    player.attack("Bullet_Basic",self.input_handle.mouse_x,self.input_handle.mouse_y)
            return

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








class InputHandler:
    def __init__(self,window):
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_button = 0
        self.keyboard = pyglet.window.key.KeyStateHandler()
        window.push_handlers(self.keyboard)
        self._currently_pressed = []

    def mouse_pressed(self,x,y,button):
        self.mouse_x = x
        self.mouse_y = y
        self._currently_pressed.append(button)

    # Is a key being click+held?
    def mouse_dragged(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def mouse_released(self, button):
        self._currently_pressed.remove(button)
    
    # Is a key currently being held down?
    def is_pressed(self, button):
        to_return = next((x for x in self._currently_pressed if x == button), None)
        return to_return != Non





        



