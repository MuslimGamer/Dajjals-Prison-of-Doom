import pyglet
import random


from pyglet.window import key, mouse
from shooter import obj
from shooter.config import Config

from math import atan2, sin, cos, degrees, pi, sqrt

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
        return to_return != None

def input(main_list, input_handle): 
    for player in main_list[0]:
        player.mx = input_handle.keyboard[key.A] * -1 + input_handle.keyboard[key.D] * 1
        player.my = input_handle.keyboard[key.S] * -1 + input_handle.keyboard[key.W] * 1

        if not (abs(player.mx) + abs(player.my) == 1):
            # If both keys are down, don't move at 1.4x; move at ~sqrt(2)/2
            player.mx = player.mx * 0.707
            player.my = player.my * 0.707

        if not (player.cooldown):
            if (input_handle.is_pressed(mouse.LEFT)):
                if Config.instance.get('melee_enabled'):
                    attack(player,"Melee",input_handle.mouse_x,input_handle.mouse_y,main_list[2])
                    player.cooldown = 10   #Todo: Add attribute to object
                else:
                    attack(player,"Basic",input_handle.mouse_x,input_handle.mouse_y,main_list[2])
                    player.cooldown = 50   #Todo: Add attribute to object    
            elif (input_handle.is_pressed(mouse.RIGHT)):
                attack(player,"Basic",input_handle.mouse_x,input_handle.mouse_y,main_list[2])
        return


def attack(source_obj,attack_type,target_x,target_y,bullet_list):
    if not (source_obj.cooldown):	#Previous cooldown timer has expired, ready to attack again.

        # Calculate the angle of the shot by using trig
        # This gives us consistent bullet speed regardless of angle
        dx = target_x - source_obj.x    
        dy = target_y - source_obj.y
        theta = atan2(dx,dy)			#Mathy goodness.
        mx = 10 * sin(theta)
        my = 10 * cos(theta)


        b = obj.spawn('Bullet',"Basic",source_obj.x+mx*source_obj.sprite.scale,source_obj.y+my*source_obj.sprite.scale)	#Spawn attack object
        b.mx = mx										#Apply motion to object
        b.my = my

        source_obj.cooldown = b.cost     	#Apply cooldown from attack.

        bullet_list.append(b)			#Enter bullet object into active list for processing
    



def collision(obj_list):
    # TODO: introduce a quadtree if we have too many objects to check collisions for
    # With AABB, we should be okay, as the performance impact is fairly minimal
    for player in obj_list[0]:				#Note: This check is intended for collision with bullets spawned by enemies. 
        for bullet in obj_list[2]:			#Attempting alternate fix by spawning bullet ahead of player in direction of shot
            AABB_Collision_Test(player, bullet)		#Spawn displacement scaled by object size.
    for enemy in obj_list[1]:
        for bullet in obj_list[2]:
            AABB_Collision_Test(enemy, bullet)

def AABB_Collision_Test(obj1, obj2):
    #Simple collision detection for on-rotated rectangles. TODO: Attempt other methods later if time.
    #Sprites tested against 4 conditions, if all pass collision detected. 
    #And conditionals short-circuit (skip if failure detected). 
    
    #Question: Does python continue processing conditionals with 'and' logic if one of the conditionals has already failed?

    #On detection, Obj1.health--, obj2.health = 0. (Despawn obj2 to prevent collision on next frame)

    if (obj1.sprite.x < obj2.sprite.x + obj2.sprite.width) and (obj1.sprite.x + obj1.sprite.width > obj2.sprite.x) and (obj1.sprite.y < obj2.sprite.y + obj2.sprite.width) and (obj1.sprite.y + obj1.sprite.height > obj2.sprite.y):
        #Todo if time: Knockback on collision? object requires attribute:mass.
        #Alternatively: use image scale as an indicator of mass?
        obj1.health = obj1.health - 1
        obj2.health = 0


def update(obj_list):
    for obj in obj_list:
        obj.x = obj.x + obj.mx
        obj.y = obj.y + obj.my
        obj.sprite.set_position(obj.x,obj.y)

        if obj.cooldown:
            obj.cooldown = obj.cooldown - 1

        if obj.health <= 0:
            obj_list.remove(obj)

        # Call your update method, if you have one
        if hasattr(obj, "update") and callable(getattr(obj, "update")):
            obj.update()
    pass
        


#Standard behavior, rush player, attack location
def agro_ai(obj, main_list):
    for player in main_list[0]:
        dx = obj.x - player.x
        dy = obj.y - player.y
        distance_from_player = sqrt(dx*dx + dy*dy)
        if (distance_from_player > 10):				#Get in close
            theta = atan2(dx,dy)		#Mathy goodness.
            obj.mx = -1 * sin(theta)
            obj.my = -1 * cos(theta)
        else:
            attack(obj,"Melee",player.x,player.y,main_list[2])	#And Punch


#Coward behavior, maintain distance, attack location
def coward_ai(obj, main_list):
    for player in main_list[0]:
        dx = obj.x - player.x
        dy = obj.y - player.y
        theta = atan2(dx,dy)			#Mathy goodness.
 
        distance_from_player = sqrt(dx*dx + dy*dy)
        if (distance_from_player < 150+random.randrange(100)):				#Get in kind of close.
            theta = theta *-0.9								#Jittery holding pattern
            attack(obj,"basic",player.x,player.y,main_list[2])	#And Punch

        obj.mx = -1 * sin(theta)
        obj.my = -1 * cos(theta)

  
   
        return

#Tank behavoir, Slower agro.
def slow_ai(obj, main_list):
    for player in main_list[0]:
        dx = obj.x - player.x
        dy = obj.y - player.y
        distance_from_player = sqrt(dx*dx + dy*dy)
        if (distance_from_player > 10):				#Get in close
            theta = atan2(dx,dy)		#Mathy goodness.
            obj.mx = -0.3 * sin(theta)
            obj.my = -0.3 * cos(theta)
        else:
            attack(obj,"Melee",player.x,player.y,main_list[2])	#And Punch
        pass

#Object is a tempoarary effect (Eg Explosion sprite). Decrease health as counter until removal.
def misc_ai(obj, main_list):
    if (obj.health > 0):
        obj.health = obj.health - 1

#No AI attached to this object
def NULL_ai(obj):
    pass

#Undefined behavior referenced.
def error_ai(obj):
    raise(Exception('Error: AI has gone rouge'))


def ai(obj_list, main_list):			#Generic AI handler
    for obj in obj_list:
        ai_action[obj.ai](obj, main_list)		#Reference dictionary against object AI variable, Vector to specific function for AI type.

ai_action={
    "agro": agro_ai,
    "coward": coward_ai,
    "slow": slow_ai,
    "NULL": NULL_ai,
    "misc": misc_ai}
