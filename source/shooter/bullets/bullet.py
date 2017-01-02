import shooter.obj
from shooter.obj import GameObject
from shooter.bullets import rocket, basic, melee, explode, railcharge
from math import atan2,atan, sin, cos, degrees, pi, sqrt
import pyglet

Bullet_Subclass = {
    'Bullet_Basic': basic,
    'Bullet_Rocket': rocket,
    'Bullet_Melee': melee,
    'Bullet_RailCharge': railcharge,
    'Explode': explode
}
class Bullet(GameObject):
    def __init__(self, owner, prototype):
        GameObject.__init__(self, owner, 'Bullet', prototype)

        self.on_death = lambda: Bullet_Subclass[self.id].on_death(self)
        self.__type = Bullet_Subclass[self.id].init(self)

    def rotate(self):
        self.thetadeg = self.theta*180/pi

   #For bullets, no rotation is ever experienced.
        #Precalc sprite offset for rotation on init to save processing time later. 
        self.spritexoffset = self.radius * sin(self.theta+self.theta_offset)
        self.spriteyoffset = self.radius * cos(self.theta+self.theta_offset)

        self.sprite.rotation = self.thetadeg +90	#Sprite rotation in degrees, while trig functions return radians (Like real maths)


    def update(self):
        self.health -= 1
        Bullet_Subclass[self.id].update(self)


    def move(self):

        self.x = self.x + self.mx
        self.y = self.y + self.my

        self.sprite_x = self.x - self.spritexoffset	#Calculate centroid position given:
        self.sprite_y = self.y - self.spriteyoffset	# Sprite Datum position/Rotation &
           										# Calculated centroid offsets from sprite aspects
        self.sprite.set_position(self.sprite_x,self.sprite_y)

        if self.health < 1:
            shooter.obj.Type_lists[self.type].remove(self)
        

