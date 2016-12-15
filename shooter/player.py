import time

from shooter import config
from shooter import obj
from shooter.weapons.gun import Gun

class Player(obj.GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        obj.GameObject.__init__(self, owner, 'Player', prototype)
        self.__gun = Gun(config.get("pistol_bullets"), config.get("pistol_reload_seconds"), "Bullet_Basic")

    def reload(self):
        self.__gun.reload()

    def is_reloading(self):
        return self.__gun.is_reloading()

    def fire(self, mouse_x, mouse_y):        
        if self.__gun.fire():
            self.attack(self.__gun.bullet_type, mouse_x, mouse_y)

    def update(self):
        self.__gun.update()

    @property
    def shots_left(self):
        return self.__gun.shots_left