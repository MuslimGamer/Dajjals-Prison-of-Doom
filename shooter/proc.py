##################################################################
## Proc.py - Processing functions     				##
##################################################################
## Functions relating to Rendering, Input and related functions ##
##################################################################

import pyglet
import random



from pyglet.window import key, mouse
from shooter import debug
import shooter.obj
from shooter import config
from shooter import file_watcher
from shooter import ui_manager
import shooter.tutorials.tutorial_manager

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
        self.score_label = None # shouldn't be here, not every screen needs one

        # Methods are all private because we need them declared before we push the handlers
        def on_mouse_press(x, y, button, modifiers):
            self.mouse_pressed(x,y,button)
            if shooter.tutorials.tutorial_manager._current_tutorial != None:
                shooter.tutorials.tutorial_manager._current_tutorial.on_click(button, x, y)

        def on_mouse_release(x,y,button, modifiers):
            self.mouse_released(button)

        def on_mouse_drag(x,y,dx,dy, buttons, modifiers):        
            self.mouse_dragged(x, y)
        
        def on_key_press(symbol, modifiers):
            if not symbol in self._currently_pressed:
                self._currently_pressed.append(symbol)

            # Call our one and only subscriber if he's there (tutorial manager)
            if self.on_press_callback != None:
                self.on_press_callback(symbol, self._currently_pressed)

            # game logic to execute when we press a key the first time only (not press+hold)
            if symbol == key.R: 
                shooter.obj.Player_list[0].reload()
            elif symbol == key.P:
                self.paused = not self.paused
                ui_manager.paused = self.paused
            elif config.get("enable_cheat_codes") == True and self.is_pressed(key.GRAVE):
                debug.ask_and_process_cheat_code(shooter.obj.Player_list[0])

        def on_key_release(symbol, modifiers):
            if symbol in self._currently_pressed:
                self._currently_pressed.remove(symbol)
        
        def on_draw():		#Kept seperate from processing callback, Frame rate not tied to simulation speed.
            self.__window.clear()

            for bg in shooter.obj.Backgrounds_list:
                bg.sprite.draw()
            for player in shooter.obj.Player_list:		#Render player sprite
                player.sprite.draw()
            for enemy in shooter.obj.Enemy_list:		#Render enemy sprites
                enemy.sprite.draw()
            for bullet in shooter.obj.Bullet_list:		#Render bullet sprites
                bullet.sprite.draw()
            for pickup in shooter.obj.Pickup_list:
                pickup.sprite.draw()
            for misc in shooter.obj.Misc_list:		#Render Misc sprites
                misc.sprite.draw()
                
            if self.draw_ui and len(shooter.obj.Player_list) >= 1:
                # First player is THE player to pass into the UI manager
                if shooter.obj.Player_list[0].id == "Player_Basic":
                    self.__ui_manager.draw(shooter.obj.Player_list[0])

            shooter.tutorials.tutorial_manager.draw()

            if self.paused:
                self.pause_sprite.draw()

            # draw score after game over. This is set to None if it's not supposed to be drawn.
            if self.score_label != None:
                self.score_label.draw()

        def on_close():
            file_watcher.stop()

        self.__window.push_handlers(on_mouse_press,on_mouse_release,on_mouse_drag,on_draw,on_close,on_key_press, on_key_release)

    def notify_on_press(self, method):
        self.on_press_callback = method

    def mouse_pressed(self,x,y,button):
        self.mouse_x = x
        self.mouse_y = y
        self._currently_pressed.append(button)
        if self.on_press_callback != None:
            self.on_press_callback(button, self._currently_pressed)

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
        if (not self.paused and not shooter.tutorials.tutorial_manager.is_showing_tutorial and len(shooter.obj.Player_list) > 0):
            player = shooter.obj.Player_list[0]
            if not(player.id == "Player_Basic"):return
            player.mousex = self.mouse_x
            player.mousey = self.mouse_y

            if config.get("control_style") == "relative":
                player.commandy = self.is_pressed(key.S) * -0.03 + self.is_pressed(key.W) * 0.1
                player.commandx = (self.is_pressed(key.A) * -1 + self.is_pressed(key.D) * 1)*0.1

                #player.mx += thrust * cos(player.theta)
                #player.my += thrust * -1*sin(player.theta)

                player.mx = player.mx *0.99
                player.my = player.my *0.99

            
            else:
                player.mx = (self.is_pressed(key.A) * -1 + self.is_pressed(key.D) * 1)*player.speed
                player.my = (self.is_pressed(key.S) * -1 + self.is_pressed(key.W) * 1)*player.speed

                if not (abs(player.mx) + abs(player.my) == 1):
                # If both keys are down, don't move at 1.4x; move at ~sqrt(2)/2
                    player.mx = player.mx * 0.707
                    player.my = player.my * 0.707

            if config.get("enable_cheat_codes") == True and self.is_pressed(key.GRAVE):
                debug.ask_and_process_cheat_code(player)

            if self.is_pressed(key.R): 
                player.reload()

            if (self.is_pressed(mouse.RIGHT)):
                if config.get('melee_enabled'):
                    if not (player.cooldown):  
                        shield = player.handle.spawn('Player',"Deflect",player.x,player.y)
                        shooter.obj.Player_list.append(shield)
                    else:
                        for deflect in shooter.obj.Player_list:
                            if deflect.id == "Deflect":
                                # center on player
                                dx = self.mouse_x - player.x
                                dy = self.mouse_y - player.y
                                # stay around player
                                deflect.theta = atan2(dx,dy)			#Mathy goodness.
                    #player.cooldown = 10 #Maintain cooldown of melee/shield if continuing 
                else:
                    # TODO: duplicate railgun code below (from elif self.is_pressed(mouse.LEFT)) here
                    # If not, railgun just straight-out fires (doesn't charge) with right key if
                    # melee is not enabled
                    player.fire(self.mouse_x, self.mouse_y) 
            elif self.is_pressed(mouse.LEFT):      
                for rail in shooter.obj.Bullet_list:
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






        



