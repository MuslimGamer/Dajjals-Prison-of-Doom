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
        self._currently_pressed = []


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
                if obj.Player_list[0].id == "Player_Basic":self.__ui_manager.draw(obj.Player_list[0])

        def on_close():
            file_watcher.stop()

        self.__window.push_handlers(on_mouse_press,on_mouse_release,on_mouse_drag,on_draw,on_close, self.keyboard)


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
        if (len(obj.Player_list)):
            player = obj.Player_list[0]
            if not(player.id == "Player_Basic"):return

            if config.get("control_style") == "relative":
                thrust = self.keyboard[key.S] * -0.01 + self.keyboard[key.W] * 0.05
                player.theta += (self.keyboard[key.A] * -1 + self.keyboard[key.D] * 1)*2*pi/180

                player.mx += thrust * cos(player.theta)
                player.my += thrust * -1*sin(player.theta)

                if (sqrt(player.mx*player.mx+player.my*player.my)>player.speed):
                    player.mx = player.mx*.9
                    player.my = player.my*.9
                player.mx = player.mx *0.99 
                player.my = player.my *0.99
            
            else:
                player.mx = self.keyboard[key.A] * -1 + self.keyboard[key.D] * 1
                player.my = self.keyboard[key.S] * -1 + self.keyboard[key.W] * 1

                if not (abs(player.mx) + abs(player.my) == 1):
                # If both keys are down, don't move at 1.4x; move at ~sqrt(2)/2
                    player.mx = player.mx * 0.707 * player.speed
                    player.my = player.my * 0.707 * player.speed

            if config.get("enable_cheat_codes") == True and self.keyboard[key.GRAVE]:
                debug.ask_and_process_cheat_code(player)

            if self.keyboard[key.R]: 
                player.reload()

            if (self.is_pressed(mouse.RIGHT)):
                if config.get('melee_enabled'):
                    if not (player.cooldown):  
                        print("Deflect")                      
                        shield = player.handle.spawn('Player',"Deflect",player.x,player.y)
                        print(shld.id)
                    else:
                        for deflect in obj.Player_list:
                            if deflect.id == "Deflect":
                                dx = self.mouse_x - player.x
                                dy = self.mouse_y - player.y
                                deflect.theta = atan2(dx,dy)			#Mathy goodness.
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






        



