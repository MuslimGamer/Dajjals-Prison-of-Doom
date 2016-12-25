from shooter.weapons import gun

class Pistol(gun.Gun):
    def __init__(self):
        gun.Gun.__init__(self, "pistol")
