##################################################################
## Proc.py - Processing functions     				##
##################################################################
## Functions relating to Rendering, Input and related functions ##
##################################################################

import pyglet
import random



from pyglet.window import key, mouse
from shooter import debug
from shooter import obj
from shooter import config
from shooter import file_watcher
from shooter import ui_manager

from math import atan2,atan, sin, cos, degrees, pi, sqrt

class Screen:			#Class handling window and window related functions (Draw, Events, Input)
    def __init__(self, width, height):
        self.offset_x = 100
        self.offset_y = 100
        self.__window = pyglet.window.Window(width, height)
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_button = 0
        self.keyboard = pyglet.window.key.KeyStateHandler()
        self._currently_pressed = [] # mouse buttons and keyboard keys

        self.paused = False
        pause_image = pyglet.image.load("images/paused.png") 
        self.pause_sprite = pyglet.sprite.Sprite(pause_image, 0, 0)
        self.pause_sprite.x = (width - self.pause_sprite.width) / 2
        self.pause_sprite.y = (height - self.pause_sprite.height) / 2

        self.__ui_manager = ui_manager.UiManager()
        self.draw_ui = True

        # TODO: scale when we have time!
        # self.__window_Scale = self.__window.height / WINDOW_HEIGHT
        #print(self.__window_Scale)

        def on_mouse_press(x, y, button, modifiers):
            self.mouse_pressed(x,y,button)
            pass #print("Mouse pressed")

        def on_mouse_release(x,y,button, modifiers):
            self.mouse_released(button)
            pass #print("Mouse released")

        def on_mouse_drag(x,y,dx,dy, buttons, modifiers):        
            self.mouse_dragged(x, y)
            pass #print("Mouse dragged")
        
        def on_key_press(symbol, modifiers):
            if not symbol in self._currently_pressed:
                self._currently_pressed.append(symbol)

            # game logic to execute when we press a key the first time only (not press+hold)
            if symbol == key.R: 
                obj.Player_list[0].reload()
            elif symbol == key.P:
                self.paused = not self.paused
                ui_manager.paused = self.paused
            elif config.get("enable_cheat_codes") == True and self.is_pressed(key.GRAVE):
                debug.ask_and_process_cheat_code(obj.Player_list[0])


        def on_key_release(symbol, modifiers):
            if symbol in self._currently_pressed:
                self._currently_pressed.remove(symbol)
        
        def on_draw():		#Kept seperate from processing callback, Frame rate not tied to simulation speed.
            self.__window.clear()

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
            for pickup in obj.Pickup_list:
                pickup.sprite.draw()

            if self.draw_ui and len(obj.Player_list) >= 1:
                # First player is THE player to pass into the UI manager
                self.__ui_manager.draw(obj.Player_list[0])

            if self.paused:
                self.pause_sprite.draw()

        def on_close():
            file_watcher.stop()

        self.__window.push_handlers(on_mouse_press,on_mouse_release,on_mouse_drag,on_draw,on_close,on_key_press, on_key_release)


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


    # NOT event driven: called frequently. If you check keys here, we constantly apply
    # this logic as long as these keys are held down. If you want something more event-driven,
    # add your code under on_key_press.
    def input(self): 
        if not self.paused:
            for player in obj.Player_list:        
                player.mx = self.is_pressed(key.A) * -1 + self.is_pressed(key.D) * 1
                player.my = self.is_pressed(key.S) * -1 + self.is_pressed(key.W) * 1

                if not (abs(player.mx) + abs(player.my) == 1):
                # If both keys are down, don't move at 1.4x; move at ~sqrt(2)/2
                    player.mx = player.mx * 0.707 * player.speed
                    player.my = player.my * 0.707 * player.speed

                if (self.is_pressed(mouse.RIGHT)):
                    if config.get('melee_enabled'):
                        if not (player.cooldown):                        
                            player.attack("Bullet_Melee",self.mouse_x,self.mouse_y)
                        else:
                            for sword in obj.Bullet_list:
                                if sword.id == "Bullet_Melee":
                                    dx = self.mouse_x - player.x
                                    dy = self.mouse_y - player.y
                                    sword.theta = atan2(dx,dy)			#Mathy goodness.
                        player.cooldown = 10 #Maintain cooldown of melee attack if attack is continueing 
                    else:
                        player.fire(self.mouse_x, self.mouse_y) 
                elif self.is_pressed(mouse.LEFT):      
                    for rail in obj.Bullet_list:
                        if rail.id == "Bullet_RailCharge":
                            dx = self.mouse_x - player.x
                            dy = self.mouse_y - player.y
                            rail.theta = atan2(dx,dy)
                            rail.health = 20
                            return
                    player.fire(self.mouse_x, self.mouse_y)

    @property
    def width(self):
        return self.__window.width

    @property
    def height(self):
        return self.__window.height






        



