import pyglet
from shooter import config

pyglet.options['audio'] = ('directsound', 'openal', 'pulse', 'silent')

pistol = pyglet.media.load("sounds/pistol.wav", streaming = False)
machine = pyglet.media.load("sounds/machine.wav", streaming = False)
explosion = pyglet.media.load("sounds/explosion.wav", streaming = False)
enemy_hit = pyglet.media.load("sounds/hitenemy.wav", streaming = False)


        
