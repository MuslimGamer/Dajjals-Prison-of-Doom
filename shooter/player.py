import time

from shooter import config
from shooter import obj

class Player(obj.GameObject):
    def __init__(self, owner, prototype):
        # call base class constructor
        obj.GameObject.__init__(self, owner, 'player', prototype)
        self.__shots_left = 15
        self.__last_shot = time.time()

    # Returns true if we actually have bullets to fire
    def fire(self):        
        if self.__shots_left > 0:
            self.__shots_left -= 1
            self.__last_shot = time.time()
            return True
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
