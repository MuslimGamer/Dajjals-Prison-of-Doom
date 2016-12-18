import time
import random

from math import atan2, sin, cos, pi, sqrt

from shooter import obj
from shooter.weapons import gun, shotgun, rocket

class Player(obj.GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        obj.GameObject.__init__(self, owner, 'Player', prototype)
        self.__gun = shotgun.Shotgun()

    def switch(self,gun_config_prefix):
        self.__gun.switch(gun_config_prefix)

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

                self.mx += 2*cos(theta+pi)			#Recoil - Obey physics, It's the law.
                self.my += 2*sin(theta+pi)			#Conservation of energy.

                self.attack(self.__gun.bullet_type, target_x, target_y)	#Spawn attack using randomly varied target location.


    def update(self):
        self.__gun.update()




    @property
    def shots_left(self):
        return self.__gun.shots_left
