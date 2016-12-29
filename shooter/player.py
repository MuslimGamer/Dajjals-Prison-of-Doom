import time
import random

from math import atan2, sin, cos, pi, sqrt
from shooter import config
from shooter import obj
from shooter.bullets import bullet
from shooter.weapons import gun, pistol, machine, shotgun, rocket, rail

class Player(obj.GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        obj.GameObject.__init__(self, owner, 'Player', prototype)
        self.__gun = pistol.Pistol()
        self.repair = 0
        self.crew  = 1
        self.drive = 0
        self.stock_speed = self.speed
        self.stock_reload = 1
        self.stock_attack = 1


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

    def reload(self):
        self.__gun.reload()

    def is_reloading(self):
        return self.__gun.is_reloading()

    def fire(self, mouse_x, mouse_y):        
        if self.__gun.fire():   #Check gun is in condition to fire (Has bullets, has cooled down, etc)

            for shot in range(self.__gun.burst_shots):  	#Repeat for number of bullets / shot.
                dx = mouse_x - self.x				#Calculate shot vector
                dy = mouse_y - self.y
                if (self.__gun.spread): spread = random.randrange(-1*self.__gun.spread,self.__gun.spread,1) * pi/180 
                else: spread = 0
								#Calculate attack vector w/Random scatter
                theta = atan2(dy, dx)+ spread 
                hyp = sqrt(dx*dx + dy*dy)

                target_x = self.x + hyp*cos(theta)			#Calculate new attack location including scatter
                target_y = self.y + hyp*sin(theta)

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
