import time
import random
import pyglet

from math import atan2, sin, cos, pi, sqrt

from shooter import config
from shooter import obj
from shooter import ui_manager
from shooter.bullets import bullet
from shooter.weapons import gun, pistol, machine, shotgun, rocket, rail

class Player(obj.GameObject):
        # call base class constructor
    def __init__(self, owner, prototype):
        obj.GameObject.__init__(self, owner, 'Player', prototype)
        self.__gun = pistol.Pistol()
        self.commandx = 0
        self.commandy = 0
        self.mousex = 0
        self.mousey = 0
        self.repair = 0
        self.crew = 1
        self.drive = 0
        self.shield = 0
        self.stock_speed = self.speed
        self.stock_reload = 1
        self.stock_attack = 1
        #self.image = pyglet.image.load(json_data['Img'])
        self.shipimage = pyglet.image.load('images/ship/ship.png')
        self.shipseq = pyglet.image.ImageGrid(self.shipimage,9,1)
        self.weaponimage = pyglet.image.load('images/ship/weapon.png')
        self.weaponseq = pyglet.image.ImageGrid(self.weaponimage,5,1)
        self.image = self.shipseq[8]
        self.imagebuff = self.shipseq[8]
        

        self.sprite = pyglet.sprite.Sprite(self.image,self.x,self.y)
        self.radius = sqrt(self.sprite.height*self.sprite.height + self.sprite.width * self.sprite.width)/2
        self.theta_offset = atan2(self.sprite.height,self.sprite.width)
        self.theta = 0

        self.sprite_x = self.x - self.radius * sin(self.theta+self.theta_offset)	#Calculate centroid position given:
        self.sprite_y = self.y - self.radius * cos(self.theta+self.theta_offset)
        self.sprite.set_position(self.sprite_x,self.sprite_y)





    def upgrade(self):
        self.repair = 0
        self.speed = self.stock_speed
        self.attackrate = self.stock_attack
        self.reloadrate = self.stock_reload
        self.__gun.reload_time_seconds = self.__gun.stock_reload_time_seconds
        self.__gun._cooldown_time_seconds = self.__gun.stock_cooldown_time_seconds
        if self.crew >= 3: self.repair = config.get('upgrades')["emergency_repairs_repair_rate"]
        if self.crew >= 6: self.speed = self.stock_speed * config.get('upgrades')["engineering_crew_speed_multiplier"]
        if self.crew >= 9: self.attackrate = config.get('upgrades')["tactics_crew_attack_rate"]
        if self.crew >= 12: self.reloadrate = config.get('upgrades')["gunner_crew_reload_rate"]
        if self.crew >= 15: self.repair = config.get('upgrades')["repair_crew_repair_rate"]
        if self.crew >= 18: self.speed = self.stock_speed * config.get('upgrades')["engine_tuning_speed_multiplier"]
        if self.crew >= 21: self.attackrate = config.get('upgrades')["weapons_tuning_attack_rate"]
        if self.crew >= 24: self.reloadrate = config.get('upgrades')["ammo_management_reload_rate"]
        if self.crew >= 27: self.speed = self.stock_speed * config.get('upgrades')["advanced_engine_tuning_speed_multiplier"]
        if self.crew >= 30: self.reloadrate = config.get('upgrades')["advanced_ammo_management_reload_rate"]
        
        self.__gun.reload_time_seconds = self.__gun.reload_time_seconds / self.reloadrate
        self.__gun._cooldown_time_seconds = self.__gun._cooldown_time_seconds / self.attackrate

    def switch(self,gun_config_prefix):
        self.__gun.switch(gun_config_prefix)
        self.upgrade()

    def set_ammo(self, ammo):
        self.__gun.__shots_left = ammo

    def reload(self):
        self.__gun.reload()

    def is_reloading(self):
        return self.__gun.is_reloading()


    def move(self):
        #Function name move is misleading: Function responsible for processing movement, rotation & object maintainance
        #if(self.mx!=0)or(self.my!=0):
        
        self.x = self.x + self.mx
        self.y = self.y + self.my

        theta = self.theta
        if self.x < 0: self.x = obj.GAME_WIDTH
        if self.x > obj.GAME_WIDTH: self.x = 0
        if self.y < 0: self.y = obj.GAME_HEIGHT
        if self.y > obj.GAME_HEIGHT: self.y = 0

        if not config.get("control_style") == "relative":theta = atan2(-self.my,self.mx)



        thrust = self.commandy
        self.theta += self.commandx


           

        if self.commandx == 0:
            if self.commandy == 0:self.imagebuff = self.shipseq[8]	#Idle
            if self.commandy > 0:self.imagebuff = self.shipseq[7]      	#Forward
            if self.commandy < 0:self.imagebuff = self.shipseq[6]      	#Backward
        elif self.commandx <0:
            if self.commandy<0:self.imagebuff = self.shipseq[1]		#Left back
            if self.commandy==0:self.imagebuff = self.shipseq[5]	#Left still
            if self.commandy>0:self.imagebuff = self.shipseq[3]		#Left forward
        elif self.commandx >0:
            if self.commandy<0:self.imagebuff = self.shipseq[0]		#Right back
            if self.commandy==0:self.imagebuff = self.shipseq[4]	#Right still
            if self.commandy>0:self.imagebuff = self.shipseq[2]		#Right Forward

        if not (self.sprite.image == self.imagebuff):self.sprite.image = self.imagebuff

        self.mx += thrust * cos(self.theta)
        self.my += thrust * -1*sin(self.theta)

                #if (sqrt(player.mx*player.mx+player.my*player.my)>player.speed):
                #    player.mx = player.mx*.9
                #    player.my = player.my*.9
        self.mx = self.mx *0.99
        self.my = self.my *0.99


        self.sprite.rotation = theta*180/pi	#Sprite rotation in degrees, while trig functions return radians (Like real maths)

        self.sprite_x = self.x - self.radius * sin(theta+self.theta_offset)	#Calculate centroid position given:
        self.sprite_y = self.y - self.radius * cos(theta+self.theta_offset)	# Sprite Datum position/Rotation &
           										# Calculated centroid offsets from sprite aspects
        self.sprite.set_position(self.sprite_x,self.sprite_y)

        if self.health < 1:
            self.health = 0
            obj.Type_lists[self.type].remove(self)
            game_over()
        
        if self.cooldown:
            self.cooldown = self.cooldown - 1



    def fire(self, mouse_x, mouse_y):        
        if self.__gun.fire():   #Check gun is in condition to fire (Has bullets, has cooled down, etc)

            for shot in range(self.__gun.burst_shots):  	#Repeat for number of bullets / shot.
                dx = mouse_x - self.x				#Calculate shot vector
                dy = mouse_y - self.y

                if (self.__gun.spread):
                    spread = random.randrange(-1*self.__gun.spread,self.__gun.spread,1) * pi/180 
                else:
                    spread = 0
				
                #Calculate attack vector w/Random scatter
                theta = atan2(dy, dx)+ spread 

                target_x = self.x + 100*cos(theta)			#Calculate new attack location including scatter
                target_y = self.y + 100*sin(theta)


                if config.get("control_style") == "relative":
                    self.mx += 0.5*cos(theta+pi)			#Recoil - Obey physics, It's the law.
                    self.my += 0.5*sin(theta+pi)			#Conservation of energy.
                else:

                    self.mx += 2*cos(theta+pi)			#Recoil - Obey physics, It's the law.
                    self.my += 2*sin(theta+pi)			#Conservation of energy.

                self.attack(self.__gun.bullet_type, target_x, target_y)	#Spawn attack using randomly varied target location.


    def update(self):
        self.__gun.update()

    def unlimited_ammo(self):
        self.__gun.cheat()

    @property
    def shots_left(self):
        return self.__gun.shots_left

    @property
    def has_won(self):
        return self.drive >= 100 * 100 # 100% x 100
