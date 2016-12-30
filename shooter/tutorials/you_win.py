import pyglet
from pyglet.window import mouse

import shooter.obj
import shooter.tutorials.speech_window
import shooter.tutorials.base_tutorial

class YouWin(shooter.tutorials.base_tutorial.BaseTutorial):
    def __init__(self, player):
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("Argh! You may have escaped, but your bretheren will not be so lucky, Muslim meat!", "dajjal")
        self.closed = False
        self.player = player

    def draw(self):
        self.window.draw()

    def update(self, key):
        if self.check_input_to_advance(key):
            self.close()

    def close(self):
        self.window.close()
        self.closed = True
        self.player.health = 0