import pyglet
from shooter import config

# Fixes a bug where audio doesn't work on Linux: prefer OpenAL over Pulse
pyglet.options['audio'] = ('directsound', 'openal', 'pulse', 'silent')

pistol = pyglet.media.load("sounds/pistol.wav", streaming = False)
machine = pyglet.media.load("sounds/machine.wav", streaming = False)
explosion = pyglet.media.load("sounds/explosion.wav", streaming = False)
enemy_hit = pyglet.media.load("sounds/hitenemy.wav", streaming = False)
rail = pyglet.media.load("sounds/rail.wav", streaming = False)
rail_fire = pyglet.media.load("sounds/railfire.wav", streaming = False)
pickup = pyglet.media.load("sounds/pickup-weapon.wav", streaming = False)
weaponreload = pyglet.media.load("sounds/reload.wav", streaming = False)
npc_pickup = pyglet.media.load("sounds/pickup-escape-pod.wav", streaming = False)
game_over = pyglet.media.load("sounds/game-over.wav", streaming = False)
you_win = pyglet.media.load("sounds/you-win.wav", streaming = False)
rail_player = pyglet.media.Player() 
rail_player.queue(rail)

# http://pyglet.readthedocs.io/en/latest/programming_guide/media.html
def play_rail():
    global rail
    global rail_player
    rail_player.queue(rail)
    rail_player.play()    

def stop_rail():
    global rail_player
    if rail_player != None:
        rail_player.pause() # stop
    rail_player = pyglet.media.Player() # reset so we can play immediately (gapless)

    # play the rail shot sound. now's the time.
    global rail_fire
    rail_fire.play()

