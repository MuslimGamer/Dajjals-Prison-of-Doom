from shooter import obj
from math import atan2, sin, cos, sqrt
import random

GridX = 8									#Set grid size. 
GridY = 8

GridSpaceX = 1024 / GridX
GridSpaceY = 576 / GridY

#Temp_AIGrid = numpy.zeros((GridX,GridY))
#AIGrid=numpy.zeros((GridX,GridY))
Temp_AIGrid = []
AIGrid = []

    
def init():									#Numpy not standard, so writing my own array initialisation
    for x in range(GridX):
        Temp_AIGrid.append([])
        AIGrid.append([])
        for y in range(GridY):
            Temp_AIGrid[x].append(0)
            AIGrid[x].append(0)


def update():									#Generate Decision gradient mesh
    for x in range(GridX):
        for y in range(GridY):
            Temp_AIGrid[x][y] = 5						#Neutral preference for empty space

    for bullet in obj.Bullet_list:
        x = int(bullet.x/GridSpaceX)
        y = int(bullet.y/GridSpaceY)
        if(x>=0 and x < GridX and y>=0 and y<GridY):Temp_AIGrid[x][y] = 0	#Avoid regions under sustained weapon fire

    for enemy in obj.Enemy_list:
        x = int(enemy.x/GridSpaceX)
        y = int(enemy.y/GridSpaceY)
        if(x>=0 and x < GridX and y>=0 and y<GridY):Temp_AIGrid[x][y]  = 3	#Move away from regions already containing enemies
										#Spread out
    for player in obj.Player_list:
        x = int(player.x/GridSpaceX)
        y = int(player.y/GridSpaceY)
        if(x>=0 and x < GridX and y>=0 and y<GridY):Temp_AIGrid[x][y]  = 20   	#Attract towards regions containing Player (Higher preference)


    for x in range(GridX):							
        for y in range(GridY):
            if(Temp_AIGrid[x][y] < 10):						#Skip elements containing NPC or player. They are always 											desireable
                accumulator = 0
                for tx in range(x-2,x+2,1):					#Select neighbouring elements to blur
                    for ty in range(y-2,y+2,1):
                        if (tx>=0 and tx<GridX and ty>=0 and ty<GridY):  	#Do not select elements outside of boundry
                            accumulator += Temp_AIGrid[tx][ty]
                AIGrid[x][y] = accumulator / 24
            else:
                AIGrid[x][y] = Temp_AIGrid[x][y]



def wander(enemy):								#Decide movements by location on gradient mesh.
    dx = enemy.destinationx - enemy.x
    dy = enemy.destinationy - enemy.y
    distance = sqrt(dx*dx+dy*dy)
    if(distance<10):
        enemy.destinationx = enemy.x+random.randrange(-50,50,1)
        enemy.destinationy = enemy.y+random.randrange(-50,50,1)
    theta = atan2(dx,dy)
    enemy.mx = enemy.speed/10* sin(theta)
    enemy.my = enemy.speed/10* cos(theta)
    ##RegionX = int(enemy.x/GridSpaceX)
    #RegionY = int(enemy.y/GridSpaceY)
    #MoveX = MoveY = 0
    #for x in range(-1,1,1):
    #    for y in range(-1,1,1):
    #        ax = RegionX+x							#Accumulater read location
    #        ay = RegionY+y
    #        if(ax>=0 and ax<GridX and ay>=0 and ay<GridY):
    #            MoveX += x*AIGrid[ax][ay]					#Accumulate movement preference scores across neighbouring
    #            MoveY += y*AIGrid[ax][ay]					#grid locations
    #theta = atan2(MoveX, MoveY)							#Set movement direction 
    #enemy.mx = enemy.speed * sin(theta)
    #enemy.my = enemy.speed * cos(theta)

def charge(enemy, target):
    dx = target.x - enemy.x
    dy = target.y - enemy.y
    theta = atan2(dx, dy)
    enemy.mx = enemy.speed* sin(theta)
    enemy.my = enemy.speed* cos(theta)

def flee(enemy, target):
    dx = enemy.x - target.x
    dy = enemy.y - target.y
    theta = atan2(dx, dy)
    enemy.mx = enemy.speed* sin(theta+1)
    enemy.my = enemy.speed* cos(theta+1)










        
