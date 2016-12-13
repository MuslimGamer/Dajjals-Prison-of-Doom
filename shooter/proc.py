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
from shooter import file_watcher

from math import atan2,atan, sin, cos, degrees, pi, sqrt

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


class Screen:			#Class handling window and window related functions (Draw, Events, Input)
    def __init__(self):
        self.window = pyglet.window.Window(width=640, height=480)
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_button = 0
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self._currently_pressed = []
        self.Window_Scale = self.window.height / WINDOW_HEIGHT
        print(self.Window_Scale)


        def on_mouse_press(x, y, button, modifiers):
            self.mouse_pressed(x,y,button)
            print("Mouse pressed")

        def on_mouse_release(x,y,button, modifiers):
            self.mouse_released(button)
            print("Mouse released")

        def on_mouse_drag(x,y,dx,dy, buttons, modifiers):        
            self.mouse_dragged(x, y)
            print("Mouse dragged")

        def on_draw():		#Kept seperate from processing callback, Frame rate not tied to simulation speed.
            self.window.clear()

            for bg in obj.Backgrounds_list:
                bg.sprite.draw()
            for player in obj.Player_list:		#Render player sprite
                player.sprite.draw()
            for enemy in obj.Enemy_list:		#Render enemy sprites
                enemy.sprite.draw()
            for bullet in obj.Bullet_list:		#Render bullet sprites
                bullet.sprite.draw()
            for misc in obj.Misc_list:		#Render Misc sprites
                misc.sprite.draw()

        def on_close():
            file_watcher.stop()

        self.window.push_handlers(on_mouse_press,on_mouse_release,on_mouse_drag,on_draw,on_close, self.keyboard)


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
        return to_return != None


    def input(self): 
        for player in obj.Player_list:
     
            player.mx = self.keyboard[key.A] * -1 + self.keyboard[key.D] * 1
            player.my = self.keyboard[key.S] * -1 + self.keyboard[key.W] * 1

            if not (abs(player.mx) + abs(player.my) == 1):
            # If both keys are down, don't move at 1.4x; move at ~sqrt(2)/2
                player.mx = player.mx * 0.707 * player.speed
                player.my = player.my * 0.707 * player.speed

            if not (player.cooldown):
                if (self.is_pressed(mouse.LEFT)):
                    if config.get('melee_enabled'):
                        player.attack("Bullet_Melee",self.mouse_x,self.mouse_y)
                    else:
                        player.attack("Bullet_Basic",self.mouse_x,self.mouse_y) 
                elif (self.is_pressed(mouse.RIGHT)):
                    player.attack("Bullet_Basic",self.mouse_x,self.mouse_y)
            elif (self.is_pressed(mouse.LEFT)):
                player.cooldown = 10 #Maintain cooldown of melee attack if attack is continueing 
            return








        



