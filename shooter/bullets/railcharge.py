import time

from shooter import sound
from shooter import player
from shooter import obj
from shooter import proc
from math import atan2,atan, sin, cos, degrees, pi, sqrt


def init(rail):
    #rail.sound.queue(sound.rail)
    #rail.sound.play()
    #sound.rail.play()
    pass  

def update(rail):

    for player in obj.Player_list:

        if rail.size < 2:rail.size += 0.003
        rail.mx = 0.01 * sin(rail.theta)	#Apply small movement to ensure sword renders with correct rotation.
        rail.my = 0.01 * cos(rail.theta)        #Position applied below instead of movement function so position updated before collsion detection
        rail.sprite.rotation = rail.theta

    # +width/2, -height/2 makes the sword perfectly center on the player
        rail.x = player.x - player.sprite.width/2 +player.radius *2* sin(rail.theta)    #Apply position immediately so factors in collision detection
        rail.y = player.y - player.sprite.height/2 +player.radius *2* cos(rail.theta) 
        return


    pass

def on_death(rail):
    sound.rail_fire.play()
    #rail.sound.queue(sound.rail_fire)#.play()
    #rail.sound.next()

    x = rail.x     #Apply position immediately so factors in collision detect
    y = rail.y
    while (x > 0 and x < obj.GAME_WIDTH and y > 0 and y < obj.GAME_HEIGHT):
        b1 = rail.handle.spawn("Bullet", 'Bullet_RailFire',x,y)
        b1.parent = rail.parent
        b1.size = rail.size
        b1.mx +=0.01*sin(rail.theta)
        b1.my +=0.01*cos(rail.theta)
        x += b1.mx*3000*b1.size
        y += b1.my*3000*b1.size
        



