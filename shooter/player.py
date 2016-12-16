import time

from shooter import obj
from shooter.weapons import gun, shotgun

class Player(obj.GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        obj.GameObject.__init__(self, owner, 'Player', prototype)
        self._gun = shotgun.Shotgun()

    def reload(self):
        self._gun.reload()

    def is_reloading(self):
        return self._gun.is_reloading()

    def fire(self, mouse_x, mouse_y):        
        if self._gun.fire():
            self.attack(self._gun.bullet_type, mouse_x, mouse_y)

    def update(self):
        self._gun.update()

    @property
    def shots_left(self):
        return self._gun.shots_left