import time

import shooter.player
import shooter.obj
from shooter import sound
from shooter import proc
from math import atan2,atan, sin, cos, degrees, pi, sqrt


def init(rail):
    pass  

def update(rail):

    for player in shooter.obj.Player_list:
        if player.id == "Player_Basic":
            #Apply small movement to ensure sword renders with correct rotation.
            #Position applied below instead of movement function so position updated before collsion detection
            if rail.size < 2:rail.size += 0.003
            rail.mx = 0.01 * sin(rail.theta)	
            rail.my = 0.01 * cos(rail.theta)        
            rail.sprite.rotation = rail.theta

        # +width/2, -height/2 makes the sword perfectly center on the player
	    #Apply position immediately so factors in collision detection
            rail.x = player.x +player.radius * 1.5* sin(rail.theta)    
            rail.y = player.y +player.radius * 1.5*cos(rail.theta) 
            return


    pass

def on_death(rail):
    for player in shooter.obj.Player_list:
        if player.id == "Player_Basic":
            player.reload()   

    step_x = 0.01*sin(rail.theta)
    step_y = 0.01*cos(rail.theta)
    scale_step_x = step_x*3000*rail.size
    scale_step_y = step_y*3000*rail.size

    x = rail.x     #Apply position immediately so factors in collision detect
    y = rail.y
    while (x > 0 and x < shooter.obj.GAME_WIDTH and y > 0 and y < shooter.obj.GAME_HEIGHT):
        b1 = rail.handle.spawn("Bullet", 'Bullet_RailFire',x,y)
        b1.parent = rail.parent
        b1.size = rail.size
        b1.mx = step_x
        b1.my = step_y
        x += scale_step_x
        y += scale_step_y
        b1.move()
        



