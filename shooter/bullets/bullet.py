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
        self.sound = pyglet.media.Player

        #self.explosion = pyglet.media.load("sounds/explosion.wav", streaming = False)
        self.on_death = lambda: Bullet_Subclass[self.id].on_death(self)
        self.__type = Bullet_Subclass[self.id].init(self)

    def update(self):
        self.health -= 1
        self.mx = sin(self.theta) * self.speed
        self.my = cos(self.theta) * self.speed
        Bullet_Subclass[self.id].update(self)
