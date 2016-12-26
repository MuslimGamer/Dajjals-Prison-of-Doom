import pyglet.sprite
import shooter.obj
import shooter.tutorials.speech_window

class StoryAndControls:
    def __init__(self):
        self.window = shooter.tutorials.speech_window.SpeechWindow()
        self.window.show("HELLO THERE. This unusually long message is brought to you by that one-eyed red ogre guy.", "dajjal")

    def draw(self):
        self.window.draw()