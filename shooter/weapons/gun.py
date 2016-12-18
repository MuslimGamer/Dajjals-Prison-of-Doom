import time

import pyglet

from shooter import config

class Gun:
    # total bullets => how many bullets before we have to reload
    # reload_time => total time (seconds) to reload
    # cooldown_time (delay between two bullets (autofire rate)) is the bullet cost in object.json
    def __init__(self, gun_config_prefix):
        self._total_shots = config.get("{0}_bullets".format(gun_config_prefix))
        self._shots_left = self._total_shots
        self.reload_time_seconds = config.get("{0}_reload_seconds".format(gun_config_prefix))
        self._cooldown_time_seconds = config.get("{0}_cooldown_seconds".format(gun_config_prefix))
        self.bullet_type = config.get("{0}_bullet_type".format(gun_config_prefix))
        self._last_shot = time.time()
        self.__audio_file = "sounds/{0}.wav".format(gun_config_prefix)

    def reload(self):
        self._shots_left = 0 # triggers auto-reload

    # Returns true if we just fired a shot
    def fire(self):
        if self._shots_left > 0 and time.time() - self._last_shot >= self._cooldown_time_seconds:
            self._shots_left -= 1
            self._last_shot = time.time()
            pyglet.media.load(self.__audio_file, streaming=False).play()
            return True
        else:
            return False

    def update(self):
        if self._shots_left == 0 and not self.is_reloading():
            self._shots_left = self._total_shots

    def is_reloading(self):
        return self._shots_left == 0 and time.time() - self._last_shot <= self.reload_time_seconds

    @property
    def shots_left(self):
        return self._shots_left