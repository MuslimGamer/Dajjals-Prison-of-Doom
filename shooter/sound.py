import pyglet
from shooter import config

#TODO: Implement array of player objects in class to allow multiple sound files to be played in paralell

class Sound:
    def __init__(self):
        self.player = pyglet.media.Player()

    def queue(self, source):
        self.player.next_source()
        self.player.queue(source)
 

    def play(self):
        self.player.play()


SoundHandler = Sound()
        
