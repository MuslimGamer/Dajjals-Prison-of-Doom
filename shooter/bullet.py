from shooter import obj
from shooter.bullets import rocket

class Bullet(obj.GameObject):
    def __init__(self, owner, prototype):
        obj.GameObject.__init__(self, owner, 'Bullet', prototype)
        print("Accessing Bullet subclass")

        Bullet_Subclass = {
            #'Bullet_basic': basic.basic,
            'Bullet_Rocket': rocket.Rocket,
        }

        self.__type = Bullet_Subclass[self.id]()
        #hself.__bull = rocket.Rocket()


   


