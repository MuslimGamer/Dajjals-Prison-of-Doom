import time

from shooter import config
from shooter import obj
from shooter.weapons.pistol import Pistol

class Player(obj.GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        obj.GameObject.__init__(self, owner, 'Player', prototype)
        self.__shots_left = 15
        self.__last_shot = time.time()
        self.__current_gun = Pistol()

    # Returns true if we actually have bullets to fire
    def reload(self):
        self.__shots_left = 0

    def fire(self, mouse_x, mouse_y):        
        if self.__shots_left > 0:
            self.__shots_left -= 1
            self.__last_shot = time.time()
            self.attack("Bullet_Basic", mouse_x, mouse_y)
        else:
            return False

    def update(self):
        if self.__shots_left == 0 and not self.is_reloading():
            self.__shots_left = config.get("pistol_bullets")

    @property
    def shots_left(self):
        return self.__shots_left

    def is_reloading(self):
        return self.__shots_left == 0 and time.time() - self.__last_shot <= config.get("pistol_reload_seconds")
