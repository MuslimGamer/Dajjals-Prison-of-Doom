
class Rocket: 
    def __init__(self):
        print("Make a rocket")
        self.on_death = lambda: explode() 

    def explode(self):
        print("Bang")
        self.handle.spawn("Bullet",'Explode',self.x,self.y)	#Spawning 2 version of object for explosion
        self.handle.spawn("Misc","explode", self.x, self.y)	#Bullet: responsible for spash damage, Misc: Cosmetic sprite to persist after explosion collision.

 
