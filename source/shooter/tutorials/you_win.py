import pyglet
from pyglet.window import mouse

import shooter.obj
import shooter.tutorials.speech_window
import shooter.tutorials.base_tutorial

class YouWin(shooter.tutorials.base_tutorial.BaseTutorial):
    def __init__(self, player):
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("Jump drive at full charge! Hit it!", "captain")
        self.window.add_button('images/next-button.png', lambda: self.update(mouse.LEFT)) # advance
        self.closed = False
        self.player = player
        self.first_text = True

    def draw(self):
        self.window.draw()

    def update(self, key):
        if self.check_input_to_advance(key):
            if self.first_text:
                self.window.show("ARGH! You may have escaped, but your bretheren will not be so lucky, Muslim meat!", "dajjal")
                self.window.clear_buttons()
                self.window.add_button('images/finish-button.png', lambda: self.close())                
                self.first_text = False
            else:
                self.close()

    def close(self):
        self.window.close()
        self.closed = True
        self.player.health = 0