import pyglet
import random


from pyglet.window import key, mouse
from shooter import obj
from shooter import config

from math import atan2,atan, sin, cos, degrees, pi, sqrt

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

        bullets = main_list[2]
        if not (player.cooldown):
            if (input_handle.is_pressed(mouse.LEFT)):
                if config.get('melee_enabled'):
                    attack(player,"Melee",input_handle.mouse_x,input_handle.mouse_y,bullets)
                    player.cooldown = 10   #Todo: Add attribute to object
                else:
                    attack(player,"Basic",input_handle.mouse_x,input_handle.mouse_y,bullets)
                    player.cooldown = 50   #Todo: Add attribute to object    
            elif (input_handle.is_pressed(mouse.RIGHT)):
                attack(player,"Basic",input_handle.mouse_x,input_handle.mouse_y,bullets)
        return


def attack(source_obj,attack_type,target_x,target_y,bullet_list):
    if source_obj.is_on_screen() and not (source_obj.cooldown):	#Previous cooldown timer has expired, ready to attack again.

        # Calculate the angle of the shot by using trig
        # This gives us consistent bullet speed regardless of angle
        dx = target_x - source_obj.x    
        dy = target_y - source_obj.y
        theta = atan2(dx,dy)			#Mathy goodness.
        mx = 10 * sin(theta)
        my = 10 * cos(theta)

        b = obj.spawn('Bullet',attack_type,source_obj.x+mx*source_obj.sprite.scale,source_obj.y+my*source_obj.sprite.scale)	#Spawn attack object
        b.parent = source_obj.id

        if attack_type == "Basic":
            b.mx = mx										#Apply motion to object if bullet
            b.my = my
        if attack_type == "Melee":
            b.x = b.x - mx*200
            b.y = b.y - my*200
            b.sprite.rotation = theta * 180/pi - 90
      


        source_obj.cooldown = b.cost     	#Apply cooldown from attack.
        bullet_list.append(b)			#Enter bullet object into active list for processing

def collision(obj_list):
    # TODO: introduce a quadtree if we have too many objects to check collisions for
    # With AABB, we should be okay, as the performance impact is fairly minimal
    players = obj_list[0]
    enemies = obj_list[1]
    bullets = obj_list[2]
    for player in players:				#Note: This check is intended for collision with bullets spawned by enemies. 
        for bullet in bullets:			#Attempting alternate fix by spawning bullet ahead of player in direction of shot
            AABB_Collision_Test(player, bullet)
        for enemy in enemies:
            AABB_Collision_Test(player, enemy)
    for enemy in enemies:
        for bullet in bullets:
            AABB_Collision_Test(enemy, bullet)

# obj1 gets hurt. obj2 dies.
def AABB_Collision_Test(obj1, obj2):
    if (obj2.parent == obj1.id):return	#Object2 was spawned by object 1. 'Stop hitting yourself'

    #Simple collision detection for on-rotated rectangles. TODO: Attempt other methods later if time.
    #On detection, Obj1.health--, obj2.health = 0. (Despawn obj2 to prevent collision on next frame)

    if (obj1.sprite.x < obj2.sprite.x + obj2.sprite.width) and (obj1.sprite.x + obj1.sprite.width > obj2.sprite.x) and (obj1.sprite.y < obj2.sprite.y + obj2.sprite.width) and (obj1.sprite.y + obj1.sprite.height > obj2.sprite.y):
        #Todo if time: Knockback on collision? object requires attribute:mass.
        #Alternatively: use image scale as an indicator of mass?
        obj1.health = obj1.health - 1
        obj2.health = 0

def update(main_list):
    for obj_type_list in main_list:
        for obj in obj_type_list:

            if(obj.mx!= 0)or(obj.my != 0):			#If object is moving
                obj.x = obj.x + obj.mx				#Update object position for calculated movement
                obj.y = obj.y + obj.my

            #Calculate sprite rotation + position(Sprite centroid, not datum) and update sprite


                theta = atan2(-obj.my,obj.mx)		#Sprite face direction of movement.
                obj.sprite.rotation = theta*180/pi	#Sprite rotation in degrees, while trig functions return radians (Like real maths)

                

                sprite_centroid_x = obj.x - obj.radius * sin(theta+obj.theta_offset)	#Calculate centroid position given:
                sprite_centroid_y = obj.y - obj.radius * cos(theta+obj.theta_offset)	# Sprite Datum position/Rotation &
           										# Calculated centroid offsets from sprite aspects
                
                obj.sprite.set_position(sprite_centroid_x,sprite_centroid_y)
            
            if obj.cooldown:
                obj.cooldown = obj.cooldown - 1

            if obj.health <= 0:
                obj_type_list.remove(obj)

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
            bullet_list = main_list[2]
            attack(obj,"Melee",player.x,player.y,bullet_list)	#And Punch


#Coward behavior, maintain distance, attack location
def coward_ai(obj, main_list):
    for player in main_list[0]:
        dx = obj.x - player.x
        dy = obj.y - player.y
        theta = atan2(dx,dy)			#Mathy goodness.
 
        distance_from_player = sqrt(dx*dx + dy*dy)
        # NOTE: ranodm here means sporadic firing when we're within d=150-250 of the player
        # This extra value should be persisted with the object somewhere for consistency
        # But, I doubt anyone will notice :)
        if (distance_from_player < 150 + random.randrange(100)):				#Get in kind of close.
            theta = theta *-0.9								#Jittery holding pattern
            bullet_list = main_list[2]
            attack(obj,"Basic",player.x-50+random.randrange(100),player.y-50+random.randrange(100),bullet_list)	#Added inaccuracy

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
            bullet_list = main_list[2]
            attack(obj,"Melee",player.x,player.y, bullet_list)	#And Punch
        pass

#Object is a tempoarary effect (Eg Explosion sprite). Decrease health as counter until removal.
def misc_ai(obj, main_list):
    if (obj.health > 0):
        obj.health = obj.health - 1

#No AI attached to this object
def NULL_ai(obj, main_list):
    pass

#Undefined behavior referenced.
def error_ai(obj, main_list):
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
