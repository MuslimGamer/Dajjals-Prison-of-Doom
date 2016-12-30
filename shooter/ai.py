import shooter.obj
from math import atan2, sin, cos, sqrt
import random

def wander(enemy):								#Decide movements by location on gradient mesh.
    dx = random.randrange(0,shooter.obj.GAME_WIDTH,1) - enemy.x
    dy = random.randrange(0,shooter.obj.GAME_HEIGHT,1) - enemy.y
    theta = atan2(dx,dy)
    enemy.mx = enemy.speed* sin(theta)
    enemy.my = enemy.speed* cos(theta)

def charge(enemy, target):
    if enemy.aicooldown &1: return
    dx = target.x - enemy.x
    dy = target.y - enemy.y
    theta = atan2(dx, dy)
    enemy.mx = enemy.speed* sin(theta)
    enemy.my = enemy.speed* cos(theta)

def flee(enemy, target):
    if enemy.aicooldown &1: return
    dx = enemy.x - target.x
    dy = enemy.y - target.y
    theta = atan2(dx, dy)
    enemy.mx = enemy.speed* sin(theta+1)
    enemy.my = enemy.speed* cos(theta+1)










        
