import time

from shooter import config

class Gun:
    # total bullets => how many bullets before we have to reload
    # reload_time => total time (seconds) to reload
    # cooldown_time (delay between two bullets (autofire rate)) is the bullet cost in object.json
    def __init__(self, gun_config_prefix):
        self.__total_shots = config.get("{0}_bullets".format(gun_config_prefix))
        self.burst_shots = config.get("{0}_burst".format(gun_config_prefix))
        self.spread = config.get("{0}_spread".format(gun_config_prefix))
        self.__shots_left = self.__total_shots
        self.reload_time_seconds = config.get("{0}_reload_seconds".format(gun_config_prefix))
        self.__cooldown_time_seconds = config.get("{0}_cooldown_seconds".format(gun_config_prefix))
        self.bullet_type = config.get("{0}_bullet_type".format(gun_config_prefix))
        self.__last_shot = time.time()

    def switch(self, gun_config_prefix):
        self.__total_shots = config.get("{0}_bullets".format(gun_config_prefix))
        self.burst_shots = config.get("{0}_burst".format(gun_config_prefix))
        self.spread = config.get("{0}_spread".format(gun_config_prefix))
        self.__shots_left = self.__total_shots
        self.reload_time_seconds = config.get("{0}_reload_seconds".format(gun_config_prefix))
        self.__cooldown_time_seconds = config.get("{0}_cooldown_seconds".format(gun_config_prefix))
        self.bullet_type = config.get("{0}_bullet_type".format(gun_config_prefix))
        self.__last_shot = time.time()

    def reload(self):
        self.__shots_left = 0 # triggers auto-reload

    # Returns true if we just fired a shot
    def fire(self):
        if self.__shots_left > 0 and time.time() - self.__last_shot >= self.__cooldown_time_seconds:
            self.__shots_left -= 1
            self.__last_shot = time.time()
            return True
        else:
            return False

    def update(self):
        if self.__shots_left == 0 and not self.is_reloading():
            self.__shots_left = self.__total_shots

    def is_reloading(self):
        return self.__shots_left == 0 and time.time() - self.__last_shot <= self.reload_time_seconds

    @property
    def shots_left(self):
        return self.__shots_left
