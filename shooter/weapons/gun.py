import time

import pyglet

from shooter import config
from shooter import sound


class Gun:
    # total bullets => how many bullets before we have to reload
    # reload_time => total time (seconds) to reload
    # cooldown_time (delay between two bullets (autofire rate)) is the bullet cost in object.json
    def __init__(self, gun_config_prefix):
        self.__total_shots = config.get("{0}_bullets".format(gun_config_prefix))
        self.burst_shots = config.get("{0}_burst".format(gun_config_prefix))
        self.spread = config.get("{0}_spread".format(gun_config_prefix))
        self.__shots_left = self.__total_shots
        self.stock_reload_time_seconds = config.get("{0}_reload_seconds".format(gun_config_prefix))
        self.reload_time_seconds = self.stock_reload_time_seconds
        self.stock_cooldown_time_seconds = config.get("{0}_cooldown_seconds".format(gun_config_prefix))
        self._cooldown_time_seconds = self.stock_cooldown_time_seconds
        self.bullet_type = config.get("{0}_bullet_type".format(gun_config_prefix))
        self._last_shot = time.time()
        self.__audio_file = "sounds/{0}.wav".format(gun_config_prefix)
        self.pew = pyglet.media.StaticSource(pyglet.media.load(self.__audio_file, streaming = False))
        self.reload_sound = pyglet.media.StaticSource(pyglet.media.load("sounds/reload.wav", streaming = False))
        self.pickup_sound = pyglet.media.StaticSource(pyglet.media.load("sounds/pickup-weapon.wav", streaming = False))

    def switch(self, gun_config_prefix):
        self.__total_shots = config.get("{0}_bullets".format(gun_config_prefix))
        self.burst_shots = config.get("{0}_burst".format(gun_config_prefix))
        self.spread = config.get("{0}_spread".format(gun_config_prefix))
        self.__shots_left = self.__total_shots
        self.stock_reload_time_seconds = config.get("{0}_reload_seconds".format(gun_config_prefix))
        self.reload_time_seconds = self.stock_reload_time_seconds
        self.stock_cooldown_time_seconds = config.get("{0}_cooldown_seconds".format(gun_config_prefix))
        self._cooldown_time_seconds - self.stock_cooldown_time_seconds
        self.bullet_type = config.get("{0}_bullet_type".format(gun_config_prefix))
        self.__audio_file = "sounds/{0}.wav".format(gun_config_prefix) 
        self.pew = pyglet.media.StaticSource(pyglet.media.load(self.__audio_file, streaming = False))
        self.pickup_sound.play

    def reload(self):
        self.__shots_left = 0 # triggers auto-reload

    # Returns true if we just fired a shot
    def fire(self):
        if self.__shots_left > 0 and time.time() - self._last_shot >= self._cooldown_time_seconds:
            self.__shots_left -= 1
            self._last_shot = time.time()
            self.pew.play()
            return True
        else:
            return False

    def update(self):
        if self.__shots_left == 0 and not self.is_reloading():
            self.__shots_left = self.__total_shots
            self.reload_sound.play

    def is_reloading(self):
        return self.shots_left == 0 and time.time() - self._last_shot <= self.reload_time_seconds

    def cheat(self):
        self.__shots_left = 999

    @property
    def shots_left(self):
        return self.__shots_left
