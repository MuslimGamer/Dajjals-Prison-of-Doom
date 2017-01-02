from shooter import sound

def init(bullet):
    pass  

def update(bullet):
    bullet.handle.spawn("Misc",'Smoke',bullet.x-bullet.mx,bullet.y-bullet.my)
    pass

def on_death(bullet):
    sound.explosion.play()
    bullet.handle.spawn("Bullet",'Explode',bullet.x,bullet.y)	#Spawning 2 version of object for explosion
    bullet.handle.spawn("Misc",'Explode', bullet.x,bullet.y)	#Bullet: responsible for spash damage, Misc: Cosmetic sprite to persist


