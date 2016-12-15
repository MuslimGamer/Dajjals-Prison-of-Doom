import time

class Gun:
    # total bullets => how many bullets before we have to reload
    # reload_time => total time (seconds) to reload
    # cooldown_time (delay between two bullets (autofire rate)) is the bullet cost in object.json
    def __init__(self, total_shots, reload_time_seconds, cooldown_time_seconds, bullet_type):
        self.__total_shots = total_shots
        self.__shots_left = total_shots
        self.reload_time_seconds = reload_time_seconds
        self.__cooldown_time_seconds = cooldown_time_seconds
        self.bullet_type = bullet_type
        self.__last_shot = time.time()

    def reload(self):
        self.__shots_left = 0 # triggers auto-reload

    # Returns true if we just fired a shot
    def fire(self):
        if self.__shots_left > 0 and (time.time() - self.__last_shot) >= self.__cooldown_time_seconds:
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